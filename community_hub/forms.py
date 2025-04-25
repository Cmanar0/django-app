from django import forms
from django.forms import inlineformset_factory
from .models import Event, TicketType, FreeTicketAllocation
from authentication.choices import MEMBERSHIP_PROGRAM_CHOICES

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'location', 
                 'category', 'is_public', 'status', 'image']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class TicketTypeForm(forms.ModelForm):
    class Meta:
        model = TicketType
        fields = ['name', 'description', 'price', 'quantity_available', 
                 'is_active', 'sale_start', 'sale_end']
        widgets = {
            'sale_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'sale_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }

class FreeTicketAllocationForm(forms.ModelForm):
    class Meta:
        model = FreeTicketAllocation
        fields = ['membership_type', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 0}),
        }

# Create formsets
TicketTypeFormSet = inlineformset_factory(
    Event, TicketType,
    form=TicketTypeForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)

FreeTicketAllocationFormSet = inlineformset_factory(
    TicketType, FreeTicketAllocation,
    form=FreeTicketAllocationForm,
    extra=len(MEMBERSHIP_PROGRAM_CHOICES),
    can_delete=False,
    min_num=0
) 