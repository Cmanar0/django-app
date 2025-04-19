from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


# ================= LOGIN VIEW =================
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


from authentication.models import UserProfile  # make sure this is imported

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'authentication/register.html', {'error': 'Passwords do not match'})

        username = email

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, 'authentication/register.html', {'error': 'Email already exists'})

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = True
        user.save()

        # Set default membership program in profile
        user_profile = user.userprofile
        user_profile.membership_program = 'member'
        user_profile.save()

        # Assign user to "member" group
        group, created = Group.objects.get_or_create(name='member')
        user.groups.add(group)

        # Send verification email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verification_link = request.build_absolute_uri(
            reverse('auth:verify_email', kwargs={'uidb64': uid, 'token': token})
        )

        message = render_to_string('authentication/verify_email.html', {
            'username': user.username,
            'verification_link': verification_link,
        })

        send_mail(
            subject='Verify your email address',
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=message,
        )

        return render(request, 'authentication/registration_pending.html', {'email': user.email})

    return render(request, 'authentication/register.html')

# ================= LOGOUT VIEW =================
def logout_view(request):
    logout(request)
    return redirect('auth:login')


# ================= VERIFY EMAIL VIEW =================
def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.userprofile.is_email_verified = True
        user.userprofile.save()
        return render(request, 'authentication/verification_success.html')

    else:
        return render(request, 'authentication/verification_failed.html')
