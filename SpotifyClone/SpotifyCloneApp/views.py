from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
# Create your views here
def index(request):
    return render(request, 'SpotifyCloneApp/index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('user_in')
        else:
            messages.info(request, 'Неправильные данные!')
            return redirect('login')

    return render(request, 'SpotifyCloneApp/login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Данный Email уже занят!')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Данный Username уже занят!')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('user_in')
        else:
            messages.info(request, 'Пароли не совпадают!')
            return redirect('signup')
    else:
        return render(request, 'SpotifyCloneApp/signup.html')

@login_required(login_url='login')
def user_in(request):
    return render(request, 'SpotifyCloneApp/user_in.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')