from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.models import UserProfile
from services.user_service import update_user_profile

# Create your views here.

@login_required(login_url='auth:login')
def dashboard_home(request):
    return render(request, 'dashboard/home.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def account(request):
    user_profile = request.user.userprofile
    membership_program_choices = UserProfile.MEMBERSHIP_PROGRAM_CHOICES
    payment_type_choices = UserProfile.PAYMENT_TYPE_CHOICES

    if request.method == 'POST':
        # Update user profile using the service function
        update_user_profile(request.user, request.POST)
        messages.success(request, 'Profile updated successfully!')

    context = {
        'user_profile': user_profile,
        'membership_program_choices': membership_program_choices,
        'payment_type_choices': payment_type_choices,
    }
    return render(request, 'dashboard/account.html', context)
