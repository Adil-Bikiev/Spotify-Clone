from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
# Create your views here
def index(request):
    return render(request, 'SpotifyCloneApp/index.html')

def login(request):
    return render(request, 'SpotifyCloneApp/login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            print('password same')
        else:
            messages.info(request, 'Пароли не совпадают!')
            return redirect('signup')
    else:
        return render(request, 'SpotifyCloneApp/signup.html')

def logout(request):
    pass