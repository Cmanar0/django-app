from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
import os

from sib_api_v3_sdk.configuration import Configuration
from sib_api_v3_sdk.api_client import ApiClient
from sib_api_v3_sdk.api.transactional_emails_api import TransactionalEmailsApi
from sib_api_v3_sdk.models import SendSmtpEmail


def send_email(subject: str, to_email: str, template_name: str, context: dict):
    """
    Generic function to send HTML email using a template via Brevo API.
    """
    message_html = render_to_string(template_name, context)

    configuration = Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')

    api_client = ApiClient(configuration)
    api_instance = TransactionalEmailsApi(api_client)

    send_smtp_email = SendSmtpEmail(
        to=[{"email": to_email}],
        subject=subject,
        html_content=message_html,
        sender={"email": os.environ.get("DEFAULT_FROM_EMAIL")}
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")


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
