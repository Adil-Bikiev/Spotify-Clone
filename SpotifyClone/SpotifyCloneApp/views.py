from django.shortcuts import render
from django.http import HttpResponse
# Create your views here
def index(request):
    return render(request, 'SpotifyCloneApp/index.html')

def login(request):
    return render(request, 'SpotifyCloneApp/login.html')

def signup(request):
    return render(request, 'SpotifyCloneApp/signup.html')

def logout(request):
    pass