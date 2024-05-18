from django.dispatch import receiver
from userauth.models import CustomUser
from appsettings.models import Preference, TemporaryPreference
from django.db.models.signals import post_save

@receiver(post_save, sender=CustomUser)
def create_preference_signal_handler(sender, instance, created, **kwargs):
    if created:
        TemporaryPreference.objects.create(user=instance)
        