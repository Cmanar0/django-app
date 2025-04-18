from django.shortcuts import redirect
from django.urls import reverse

class StaffAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        user = request.user

        # 🔒 Block non-staff from community hub
        if path.startswith('/community-hub/'):
            if not user.is_authenticated or not (user.is_staff or user.is_superuser):
                return redirect(reverse('auth:login'))

        # 🔒 Block staff/superuser from dashboard
        if path.startswith('/dashboard/'):
            if user.is_authenticated and (user.is_staff or user.is_superuser):
                return redirect(reverse('community_hub:home'))

        return self.get_response(request)
