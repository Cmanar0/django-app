from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_email_verified', 'full_name', 'company_name', 'phone', 'linkedin', 'website', 'instagram', 'street', 'city', 'country', 'membership_program', 'payment_type']
    search_fields = ['user__username', 'user__email']
    list_filter = ['is_email_verified']
