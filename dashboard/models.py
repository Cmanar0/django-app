from django.db import models
from authentication.models import UserProfile

class Payment(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=UserProfile.PAYMENT_TYPE_CHOICES)
    paid_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
