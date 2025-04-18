from django.shortcuts import redirect
from django.urls import reverse

class StaffAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/community-hub/'):
            user = request.user
            if not user.is_authenticated or not (user.is_staff or user.is_superuser):
                return redirect(reverse('login'))
        return self.get_response(request)
