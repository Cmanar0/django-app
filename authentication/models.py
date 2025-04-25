from django.db import models
from django.contrib.auth.models import User
from community_hub.models import Event, TicketType
from .choices import MEMBERSHIP_PROGRAM_CHOICES, PAYMENT_TYPE_CHOICES

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_email_verified = models.BooleanField(default=False)

    # Basic identity
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    
    # Contact
    phone = models.CharField(max_length=30, blank=True)

    # Socials
    linkedin = models.URLField(blank=True)
    website = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

    # Address
    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    # Membership info
    membership_program = models.CharField(
        max_length=20, choices=MEMBERSHIP_PROGRAM_CHOICES, default='member'
    )
    payment_type = models.CharField(
        max_length=20, choices=PAYMENT_TYPE_CHOICES, blank=True
    )

    # Tickets
    purchased_tickets = models.JSONField(default=dict, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    # Payment logic (to be handled by a related model)
    # - PaymentHistory: foreign key or M2M to Payment model (not yet implemented)
    # - MissingPayments: could be calculated or stored separately if needed

    def get_free_tickets(self):
        """Returns the number of free tickets based on membership type"""
        free_tickets = {
            'member': 0,
            'individual': 1,
            'sponsor': 2,
            'main_sponsor': 4
        }
        return free_tickets.get(self.membership_program, 0)

    def __str__(self):
        return self.user.username

class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.PROTECT)
    ticket_id = models.CharField(max_length=50, unique=True)
    num_tickets = models.IntegerField(default=1)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'event']

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.ticket_type.name}"
