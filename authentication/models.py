from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]

    MEMBERSHIP_PROGRAM_CHOICES = [
        ('member', 'Member'),
        ('individual', 'Individual Member'),
        ('sponsor', 'Sponsor'),
        ('main_sponsor', 'Main Sponsor'),
    ]

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

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    # Payment logic (to be handled by a related model)
    # - PaymentHistory: foreign key or M2M to Payment model (not yet implemented)
    # - MissingPayments: could be calculated or stored separately if needed

    def __str__(self):
        return self.user.username
