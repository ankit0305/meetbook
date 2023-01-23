from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile 
from django.contrib.auth import authenticate

# Create your views here.

def index(request):
    return render(request, 'index.html')
    #return HttpResponse("<h1>Welcome to Meetbook</h1>")
    
def signup(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "email exists")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "username exists")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                #creates user but not profle
                user.save()
                
                #login user and redirects to settings page
                #create profile for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user = user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signup')              
        else:
            messages.info(request, "password not matching")
            return redirect('signup')
    else:
        return render(request, 'signup.html')
    
def signin(request):
    if(request.method == 'POST'):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user_exists_flag = User.objects.filter(username=username).exists()
        # user_db = User.objects.filter(username=username).first()
        # pass_db = User.objects.filter(password=password).first()
        # print(user_db,pass_db)
        #checks if username or password is blank
        if(username == '' or password == ''):
            messages.info(request, "Username and Passwords are mandatory")
            return redirect('signin')
        
        #checks if username exists
        elif(user_exists_flag == False):
            messages.info(request, "User does not exists")
            return redirect('signin')
        
        #checks if credentials exists
        elif(user_exists_flag == True):
            user = authenticate(username=username, password=password)
            if user is not None:
                return redirect('index')
            else:
                messages.info(request, "Bad Credentials")
                return redirect('signin')
        else:
            return render(request, 'signin.html')
        
    else:
        return render(request, 'signin.html')