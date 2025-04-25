from django.contrib import admin
from .models import Event, EventImage

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 3

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_date', 'end_date', 'location', 'status', 'is_public')
    list_filter = ('category', 'status', 'is_public')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    inlines = [EventImageInline]
    
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

@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ('event', 'image')
    list_filter = ('event',)
    search_fields = ('event__title',)
