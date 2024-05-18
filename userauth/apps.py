from django.apps import AppConfig


class UserauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userauth'
    
    def ready(self):
        from .signals import (
            CreateUserProfile,
            SendOTP,
            CreatePreferences,
            TransferProfileData ,
            TransferPreferenceData,
            OnUserLogin
            )
