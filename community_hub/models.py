from django.db import models
from django.utils.text import slugify
from django.urls import reverse

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

class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='event_gallery/')
    
    def __str__(self):
        return f"Image for {self.event.title}"
