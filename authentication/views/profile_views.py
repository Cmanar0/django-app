from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from authentication.models import UserProfile
from services.user_service import update_user_profile

@login_required
def profile_update_view(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        # Update user profile using the service function
        update_user_profile(request.user, request.POST)
        messages.success(request, 'Profile updated successfully.')
        return redirect('auth:profile_update')

    return render(request, 'authentication/profile_update.html', {'profile': profile})


@login_required
def delete_account_view(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('auth:login')

    return render(request, 'authentication/confirm_delete.html')
