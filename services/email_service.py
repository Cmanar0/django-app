from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse


def send_email(subject: str, to_email: str, template_name: str, context: dict):
    """
    Generic function to send HTML email using a template.
    """
    message = render_to_string(template_name, context)

    send_mail(
        subject=subject,
        message='',  # leave empty if using html_message
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        html_message=message,
    )


def send_verification_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verification_link = request.build_absolute_uri(
        reverse('auth:verify_email', kwargs={'uidb64': uid, 'token': token})
    )

    context = {
        'username': user.username,
        'verification_link': verification_link,
    }

    send_email(
        subject='Verify your email address',
        to_email=user.email,
        template_name='emails/verify_email.html',
        context=context,
    )


def send_password_reset_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = request.build_absolute_uri(
        reverse('auth:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    )

    context = {
        'username': user.username,
        'reset_link': reset_link,
    }

    send_email(
        subject='Reset your password',
        to_email=user.email,
        template_name='emails/password_reset_email.html',
        context=context,
    )


def send_password_reset_confirmation_email(user):
    context = {
        'username': user.username,
    }

    send_email(
        subject='Your password was changed',
        to_email=user.email,
        template_name='emails/password_reset_confirmed.html',
        context=context,
    )
