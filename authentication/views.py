from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard:home')
        else:
            return render(request, 'authentication/login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'authentication/login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if passwords match
        if password != confirm_password:
            return render(request, 'authentication/register.html', {'error': 'Passwords do not match'})
        
        # Use email as username
        username = email
        
        # Check if username (email) already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'authentication/register.html', {'error': 'Email already exists'})
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'authentication/register.html', {'error': 'Email already exists'})
        
        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('dashboard:home')
    
    return render(request, 'authentication/register.html')

def logout_view(request):
    logout(request)
    return redirect('auth:login')
