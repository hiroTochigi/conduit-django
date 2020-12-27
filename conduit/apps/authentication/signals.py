from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from conduit.apps.profiles.models import Profile

# Register created_related_profile function by using receiver decorator
@receiver(post_save, sender=User)
def created_related_profile(sender, instance, created, *ags, **kwargs):
    """
    Create profile if the user is created
    """

    # User object is saved -> if the user object exists and 
    # the user is created this time (created is True)
    # create Profile object by using instance (current user object)
    # Then store it into the current user profile attribute (profile is not defined yet)
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)