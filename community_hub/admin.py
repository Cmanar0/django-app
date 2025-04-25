from django.contrib import admin
from .models import Event, EventImage, TicketType, FreeTicketAllocation, MembershipTicketBenefit
from authentication.models import EventRegistration

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1

class FreeTicketAllocationInline(admin.TabularInline):
    model = FreeTicketAllocation
    extra = 1

class TicketTypeInline(admin.TabularInline):
    model = TicketType
    extra = 1

class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ('registration_date', 'ticket_id')
    fields = ('user', 'ticket_type', 'num_tickets', 'registration_date', 'ticket_id', 'is_active')
    can_delete = False

class MembershipTicketBenefitInline(admin.TabularInline):
    model = MembershipTicketBenefit
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'location', 'category', 'status', 'is_public', 'get_registration_count']
    list_filter = ['category', 'status', 'is_public']
    search_fields = ['title', 'description', 'location']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [EventImageInline, TicketTypeInline, EventRegistrationInline, MembershipTicketBenefitInline]
    
    def get_registration_count(self, obj):
        return obj.eventregistration_set.count()
    get_registration_count.short_description = 'Registrations'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'image')
        }),
        ('Event Details', {
            'fields': ('start_date', 'end_date', 'location', 'category')
        }),
        ('Status', {
            'fields': ('status', 'is_public')
        }),
    )

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'price', 'max_guests']
    list_filter = ['event']
    search_fields = ['name', 'description', 'event__title']
    list_editable = ['price', 'max_guests']
    inlines = [FreeTicketAllocationInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('event', 'name', 'description', 'price', 'max_guests')
        }),
    )

@admin.register(FreeTicketAllocation)
class FreeTicketAllocationAdmin(admin.ModelAdmin):
    list_display = ['ticket_type', 'membership_type', 'quantity']
    list_filter = ['membership_type', 'ticket_type__event']
    search_fields = ['ticket_type__name', 'ticket_type__event__title']
    list_editable = ['quantity']

@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ('event', 'image')
    list_filter = ('event',)
    search_fields = ('event__title',)

@admin.register(MembershipTicketBenefit)
class MembershipTicketBenefitAdmin(admin.ModelAdmin):
    list_display = ('membership_type', 'ticket_type', 'event', 'free_ticket_count')
    list_filter = ('membership_type', 'event')
    search_fields = ('ticket_type__name', 'event__title')
