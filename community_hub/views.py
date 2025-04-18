from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def admin_home(request):
    return render(request, 'community_hub/home.html')
