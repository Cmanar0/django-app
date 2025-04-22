from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from services.email_service import update_user_in_brevo_list

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
            verified=True  # <== new
        )

        return render(request, 'authentication/verification_success.html')
    else:
        return render(request, 'authentication/verification_failed.html')
