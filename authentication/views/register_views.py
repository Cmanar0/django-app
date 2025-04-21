from django.shortcuts import render
from django.contrib.auth.models import User, Group
from services.email_service import send_verification_email, add_user_to_brevo_list


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

        # ✅ Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = True
        user.save()

        # ✅ Update user profile
        profile = user.userprofile
        profile.membership_program = 'member'
        profile.save()

        # ✅ Assign to 'member' group
        group, _ = Group.objects.get_or_create(name='member')
        user.groups.add(group)

        # ✅ Send email verification
        send_verification_email(user, request)

        # ✅ Add to Brevo contacts list
        add_user_to_brevo_list(email=email)

        return render(request, 'authentication/registration_pending.html', {'email': user.email})

    return render(request, 'authentication/register.html')
