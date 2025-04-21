from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from authentication.models import UserProfile
from services.email_service import update_user_in_brevo_list

@login_required
def profile_update_view(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        profile.first_name = request.POST.get('first_name', '')
        profile.last_name = request.POST.get('last_name', '')
        profile.company_name = request.POST.get('company_name', '')
        profile.phone = request.POST.get('phone', '')
        profile.linkedin = request.POST.get('linkedin', '')
        profile.website = request.POST.get('website', '')
        profile.instagram = request.POST.get('instagram', '')
        profile.street = request.POST.get('street', '')
        profile.city = request.POST.get('city', '')
        profile.country = request.POST.get('country', '')
        profile.membership_program = request.POST.get('membership_program', 'member')
        profile.payment_type = request.POST.get('payment_type', '')

        profile.save()

        # 🔄 Sync to Brevo
        update_user_in_brevo_list(
            email=request.user.email,
            first_name=profile.first_name,
            last_name=profile.last_name,
            company_name=profile.company_name,
            phone=profile.phone,
            membership_program=profile.membership_program,
            payment_type=profile.payment_type
        )

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
