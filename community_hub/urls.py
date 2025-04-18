from django.urls import path
from .views import admin_home

app_name = 'community_hub'

urlpatterns = [
    path('', admin_home, name='home'),
]
