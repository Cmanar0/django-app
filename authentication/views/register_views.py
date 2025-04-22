from django.shortcuts import render
from django.contrib.auth.models import User, Group
from services.email_service import send_verification_email, add_user_to_brevo_list


def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        agreed = request.POST.get('agree_policy')

        if not agreed:
            return render(request, 'authentication/register.html', {'error': 'You must agree to the terms and privacy policy.'})

        if password != confirm_password:
            return render(request, 'authentication/register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            return render(request, 'authentication/register.html', {'error': 'Email already exists'})

        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = True
        user.save()

        profile = user.userprofile
        profile.membership_program = 'member'
        profile.save()

        group, _ = Group.objects.get_or_create(name='member')
        user.groups.add(group)

        send_verification_email(user, request)
        add_user_to_brevo_list(email=email)

        return render(request, 'authentication/registration_pending.html', {'email': user.email})

    return render(request, 'authentication/register.html')
