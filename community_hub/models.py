from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from authentication.choices import MEMBERSHIP_PROGRAM_CHOICES

# Create your models here.

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('networking', 'Networking'),
        ('seminar', 'Seminar'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    is_public = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('community_hub:event_detail', kwargs={'slug': self.slug})
    
    class Meta:
        ordering = ['-start_date']

class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/')
    caption = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"Image for {self.event.title}"

class TicketType(models.Model):
    event = models.ForeignKey(Event, related_name='ticket_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    max_guests = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.name} - {self.event.title}"
    
    class Meta:
        ordering = ['price']

class MembershipTicketBenefit(models.Model):
    event = models.ForeignKey(Event, related_name='membership_benefits', on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=50, choices=MEMBERSHIP_PROGRAM_CHOICES)
    ticket_type = models.ForeignKey(TicketType, related_name='membership_benefits', on_delete=models.CASCADE)
    free_ticket_count = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.get_membership_type_display()} - {self.ticket_type.name} ({self.free_ticket_count})"
    
    class Meta:
        unique_together = ['event', 'membership_type', 'ticket_type']

class FreeTicketAllocation(models.Model):
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name='free_ticket_allocations')
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_PROGRAM_CHOICES)
    quantity = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['ticket_type', 'membership_type']
    
    def __str__(self):
        return f"{self.ticket_type.name} - {self.membership_type} - {self.quantity} free"
