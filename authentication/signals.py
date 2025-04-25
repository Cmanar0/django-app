from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from django.contrib.auth.models import User

# This signal automatically creates a UserProfile whenever a new User is created
# Django signals allow certain senders to notify a set of receivers that some action has taken place
# The post_save signal is sent after a model's save() method is called
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # Only create a profile if this is a newly created user (not an update to an existing user)
    if created:
        # Create a new UserProfile instance and associate it with the newly created User
        profile = UserProfile.objects.create(user=instance)
        
        # Automatically verify email for staff users
        # This is a convenience feature so staff don't need to verify their email
        # Regular users will still need to verify their email through the verification link
        if instance.is_staff:
            profile.is_email_verified = True
            profile.save()
