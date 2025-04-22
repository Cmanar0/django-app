from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from services.email_service import update_user_in_brevo_list, send_verification_email
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.userprofile.is_email_verified = True
        user.userprofile.save()

        # ✅ Update contact as verified in Brevo
        update_user_in_brevo_list(
            email=user.email,
            first_name=user.userprofile.first_name,
            last_name=user.userprofile.last_name,
            company_name=user.userprofile.company_name,
            phone=user.userprofile.phone,
            membership_program=user.userprofile.membership_program,
            payment_type=user.userprofile.payment_type,
            verified=True
        )

        return render(request, 'authentication/verification_success.html')
    else:
        return render(request, 'authentication/verification_failed.html')



def resend_verification_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No user with this email found.')
            return redirect('auth:login')

        if user.userprofile.is_email_verified:
            messages.info(request, 'Your email is already verified.')
            return redirect('auth:login')

        send_verification_email(user, request)
        messages.success(request, 'Verification email has been resent.')
        return redirect('auth:login')

    return redirect('auth:login')