from django.db.models.signals import post_save
from django.contrib.auth.models import User # sender - sending the signal
from django.dispatch import receiver # receiver - a function that gets the signal and performs task
from .models import Profile

"""
when user creates an account, this will also create a profile for the user's account.
"""

# when a user is saved, send this signal. 
# this signal will be received by this receiver.
# this receiver is this create_profile function.
# this create_profile function will take all of these arguments.
@receiver(post_save, sender=User) 
def create_profile(sender, instance, created, **kwargs):
    # if user was created, then create a profile object with the user equal to the instance of user that was created.
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User) 
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
