from django.db import models
from django.contrib.auth.models import User
from authentication.choices import PAYMENT_TYPE_CHOICES

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    payment_date = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.payment_date}"
