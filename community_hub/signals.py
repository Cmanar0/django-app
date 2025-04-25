from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Event

@receiver(pre_save, sender=Event)
def update_event_slug(sender, instance, **kwargs):
    """
    Signal to automatically update the slug when the title changes.
    This ensures the slug is always in sync with the title.
    """
    if instance.title and not instance.slug:
        instance.slug = slugify(instance.title)
        # Check if the slug already exists
        original_slug = instance.slug
        counter = 1
        while Event.objects.filter(slug=instance.slug).exclude(pk=instance.pk).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1
    elif instance.title and instance.slug and not instance.slug.startswith(slugify(instance.title)):
        # If title has changed, update the slug
        base_slug = slugify(instance.title)
        instance.slug = base_slug
        # Check if the new slug already exists
        original_slug = instance.slug
        counter = 1
        while Event.objects.filter(slug=instance.slug).exclude(pk=instance.pk).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1 