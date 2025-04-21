from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
import os

from sib_api_v3_sdk.configuration import Configuration
from sib_api_v3_sdk.api_client import ApiClient
from sib_api_v3_sdk.api.transactional_emails_api import TransactionalEmailsApi
from sib_api_v3_sdk.api.contacts_api import ContactsApi
from sib_api_v3_sdk.models import SendSmtpEmail, CreateContact


def send_email(subject: str, to_email: str, template_name: str, context: dict):
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


def add_user_to_brevo_list(email: str, first_name: str = '', last_name: str = '', company_name: str = '', phone: str = '', membership_program: str = '', payment_type: str = '', list_ids: list[int] = [3]):
    configuration = Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')

    with ApiClient(configuration) as api_client:
        api_instance = ContactsApi(api_client)
        contact = CreateContact(
            email=email,
            list_ids=list_ids,
            attributes={
                "FIRSTNAME": first_name,
                "LASTNAME": last_name,
                "COMPANY": company_name,
                "PHONE": phone,
                "MEMBERSHIP": membership_program,
                "PAYMENT": payment_type
            },
            update_enabled=True
        )
        try:
            api_instance.create_contact(contact)
        except Exception as e:
            print(f"Error adding user to Brevo list: {e}")


def update_user_in_brevo_list(email: str, first_name: str = '', last_name: str = '', company_name: str = '', phone: str = '', membership_program: str = '', payment_type: str = ''):
    configuration = Configuration()
    configuration.api_key['api-key'] = os.environ.get('BREVO_API_KEY')

    with ApiClient(configuration) as api_client:
        api_instance = ContactsApi(api_client)
        contact = CreateContact(
            email=email,
            attributes={
                "FIRSTNAME": first_name,
                "LASTNAME": last_name,
                "COMPANY": company_name,
                "PHONE": phone,
                "MEMBERSHIP": membership_program,
                "PAYMENT": payment_type
            },
            update_enabled=True
        )
        try:
            api_instance.create_contact(contact)
        except Exception as e:
            print(f"Error updating Brevo contact: {e}")
