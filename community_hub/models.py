from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from authentication.choices import MEMBERSHIP_PROGRAM_CHOICES

# Create your models here.

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('music', 'Music'),
        ('community', 'Community'),
        ('education', 'Education'),
        ('health', 'Health'),
        ('business', 'Business'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    is_public = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('community_hub:event_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Check if the slug already exists
            original_slug = self.slug
            counter = 1
            while Event.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

class TicketType(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_types')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)  # 0 means unlimited
    is_active = models.BooleanField(default=True)
    sale_start = models.DateTimeField(null=True, blank=True)
    sale_end = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.event.title}"
    
    class Meta:
        ordering = ['price']
    
    def get_free_tickets_for_membership(self, membership_type):
        """Get the number of free tickets for a specific membership type"""
        try:
            allocation = this.free_ticket_allocations.get(membership_type=membership_type)
            return allocation.quantity
        except FreeTicketAllocation.DoesNotExist:
            return 0

class FreeTicketAllocation(models.Model):
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name='free_ticket_allocations')
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_PROGRAM_CHOICES)
    quantity = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ['ticket_type', 'membership_type']
    
    def __str__(self):
        return f"{self.ticket_type.name} - {self.membership_type} - {self.quantity} free"

class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='event_gallery/')
    
    def __str__(self):
        return f"Image for {self.event.title}"
