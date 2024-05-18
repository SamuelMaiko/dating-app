from django.db import models
from django.conf import settings

User=settings.AUTH_USER_MODEL


class Preference(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'Male', 'Male'
        FEMALE = 'Female', 'Female'
        OTHER = 'Other', 'Other'
        
    class DenominationChoices(models.TextChoices):
        CATHOLIC='Catholic','Catholic'
        ADVENTIST='Adventist','Adventist'
        ISLAMIC='Islamic','Islamic'
        PROTESTANT='Protestant','Protestant'
        OTHER='Other','Other'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preference")
    min_age = models.IntegerField(default=18)
    max_age = models.IntegerField(default=100)
    location = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, null=True)
    denomination = models.CharField(max_length=10, choices=DenominationChoices.choices, blank=True, null=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"
    
    class Meta:
        db_table="preferences"
