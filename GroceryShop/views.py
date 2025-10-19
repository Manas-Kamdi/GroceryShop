# views.py
from django.core.signals import request_started
from django.shortcuts import render

def home(request):
    return render(request, "Home.html")

def login(request):
    return render(request,"login.html")

def signup(request):
    return render(request,"signup.html")

def navbar(request):
    return render(request,"Navbar.html")