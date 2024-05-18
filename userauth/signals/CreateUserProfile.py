from django.dispatch import receiver
from userauth.models import CustomUser
from profiles.models import UserProfile, TemporaryProfile
from django.db.models.signals import post_save

@receiver(post_save, sender=CustomUser)
def create_profile_signal_handler(sender, instance, created, **kwargs):
    if created:
        TemporaryProfile.objects.create(user=instance)
        