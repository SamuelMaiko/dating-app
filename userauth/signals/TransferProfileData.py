from django.db.models.signals import Signal
from django.dispatch import receiver
from profiles.models import UserProfile, TemporaryProfile

transfer_profile_data_signal = Signal()

@receiver(transfer_profile_data_signal, sender=None)
def transfer_profile_data(sender, **kwargs):
    user = kwargs.get('user')

    if user:
        try:
            temporary_profile = user.temporary_profile
        except TemporaryProfile.DoesNotExist:
            return

        # Create a new instance of the permanent profile
        profile = UserProfile.objects.create(
            user=user,
            date_of_birth=temporary_profile.date_of_birth,
            denomination=temporary_profile.denomination,
            gender=temporary_profile.gender,
            location=temporary_profile.location,
            profile_picture=temporary_profile.profile_picture,
            bio=temporary_profile.bio
        )

        # Delete the temporary profile
        temporary_profile.delete()
        
        user.transfer_completed=True
        user.save()
