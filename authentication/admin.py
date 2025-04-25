from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, EventRegistration
from services.email_service import send_verification_email, send_password_reset_email

class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ('registration_date', 'ticket_id')
    fields = ('event', 'num_tickets', 'registration_date', 'ticket_id', 'is_active')
    can_delete = False

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, EventRegistrationInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'get_email_verified', 'get_event_count')
    list_filter = ('is_staff', 'is_active', 'userprofile__is_email_verified')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    def get_email_verified(self, obj):
        return obj.userprofile.is_email_verified
    get_email_verified.short_description = 'Email Verified'
    get_email_verified.boolean = True
    
    def get_event_count(self, obj):
        return obj.eventregistration_set.count()
    get_event_count.short_description = 'Events Registered'
    
    actions = ['resend_verification_email', 'send_password_reset']
    
    def resend_verification_email(self, request, queryset):
        for user in queryset:
            if not user.userprofile.is_email_verified:
                send_verification_email(user, request)
        self.message_user(request, f"Verification emails sent to {queryset.count()} users.")
    resend_verification_email.short_description = "Resend verification email"
    
    def send_password_reset(self, request, queryset):
        for user in queryset:
            send_password_reset_email(user, request)
        self.message_user(request, f"Password reset emails sent to {queryset.count()} users.")
    send_password_reset.short_description = "Send password reset email"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_email_verified', 'first_name', 'last_name', 'company_name', 'phone', 'membership_program', 'payment_type', 'created_at', 'get_event_count']
    search_fields = ['user__username', 'user__email', 'first_name', 'last_name', 'company_name']
    list_filter = ['is_email_verified', 'membership_program', 'payment_type']
    readonly_fields = ['created_at']
    
    def get_event_count(self, obj):
        return obj.user.eventregistration_set.count()
    get_event_count.short_description = 'Events Registered'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'is_email_verified')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'company_name', 'phone')
        }),
        ('Social Media', {
            'fields': ('linkedin', 'website', 'instagram')
        }),
        ('Address', {
            'fields': ('street', 'city', 'country')
        }),
        ('Membership', {
            'fields': ('membership_program', 'payment_type')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        })
    )
    
    actions = ['verify_emails']
    
    def verify_emails(self, request, queryset):
        for profile in queryset:
            profile.is_email_verified = True
            profile.save()
        self.message_user(request, f"{queryset.count()} profiles marked as email verified.")
    verify_emails.short_description = "Mark selected profiles as email verified"

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'num_tickets', 'registration_date', 'ticket_id', 'is_active']
    list_filter = ['is_active', 'registration_date', 'event']
    search_fields = ['user__username', 'user__email', 'event__title', 'ticket_id']
    readonly_fields = ['registration_date', 'ticket_id']
    ordering = ['-registration_date']

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
