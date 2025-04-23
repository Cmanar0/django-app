from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordResetConfirmView

from services.email_service import (
    send_verification_email,
    send_password_reset_email,
    send_password_reset_confirmation_email,
    add_user_to_brevo_list
)
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


def password_reset_request_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            send_password_reset_email(user, request)
            messages.success(request, "Password reset link has been sent.")
            return redirect('auth:password_reset_done')
        else:
            messages.error(request, "No user found with that email.")

    return render(request, 'authentication/password_reset_form.html')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/password_reset_confirm.html'
    success_url = reverse_lazy('auth:password_reset_complete')

    def form_valid(self, form):
        print("✅ form_valid: password updated for user:", self.user.email)
        send_password_reset_confirmation_email(self.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("⛔ form_invalid:", form.errors)
        return super().form_invalid(form)
