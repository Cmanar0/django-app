from django import forms
from django.forms import inlineformset_factory
from .models import Event, TicketType, FreeTicketAllocation, MembershipTicketBenefit
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
        fields = ['name', 'description', 'price', 'max_guests']
        widgets = {
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
    fields=('name', 'price', 'description', 'max_guests'),
    extra=1,
    can_delete=True
)

FreeTicketAllocationFormSet = inlineformset_factory(
    TicketType, FreeTicketAllocation,
    form=FreeTicketAllocationForm,
    extra=len(MEMBERSHIP_PROGRAM_CHOICES),
    can_delete=False,
    min_num=0
)

MembershipTicketBenefitFormSet = inlineformset_factory(
    Event,
    MembershipTicketBenefit,
    fields=('membership_type', 'ticket_type', 'free_ticket_count'),
    extra=1,
    can_delete=True
) 