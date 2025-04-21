from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from services.email_service import send_verification_email, add_user_to_brevo_list
from authentication.models import UserProfile


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.userprofile.is_email_verified and not user.is_superuser:
                return render(request, 'authentication/login.html', {
                    'error': 'Please verify your email before logging in.'
                })

            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('community_hub:home')
            return redirect('dashboard:home')
        else:
            return render(request, 'authentication/login.html', {'error': 'Invalid username or password'})

    return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    return redirect('auth:login')
