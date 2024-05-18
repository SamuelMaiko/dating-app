from django.db.models.signals import Signal
from django.dispatch import receiver
from appsettings.models import Preference, TemporaryPreference

transfer_preference_data_signal = Signal()

@receiver(transfer_preference_data_signal, sender=None)
def transfer_preference_data(sender, **kwargs):
    user = kwargs.get('user')

    if user:
        try:
            temporary_preference = user.temporary_preference
        except TemporaryPreference.DoesNotExist:
            return

        # Create a new instance of the permanent preference
        preference = Preference.objects.create(
            user=user,
            min_age=temporary_preference.min_age,
            max_age=temporary_preference.max_age,
            location=temporary_preference.location,
            gender=temporary_preference.gender,
            denomination=temporary_preference.denomination
        )

        # Delete the temporary preference
        temporary_preference.delete()
        
        user.transfer_completed=True
        user.save()     
