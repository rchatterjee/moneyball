from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def logged_in(request):
    return render(request, 'logged-in.html')

def login_error(request):
    return render(request, 'login-error.html')
