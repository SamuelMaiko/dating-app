from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .TransferProfileData import transfer_profile_data_signal
from .TransferPreferenceData import transfer_preference_data_signal

@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    if not user.transfer_completed:  # Assuming transfer_completed is a boolean field in the User model
        # Dispatch the signal to transfer data only if it's the user's first login
        transfer_profile_data_signal.send(sender=None, user=user)
        transfer_preference_data_signal.send(sender=None, user=user)
