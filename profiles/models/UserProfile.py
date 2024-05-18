from django.db import models
from userauth.models import CustomUser
from datetime import date

class UserProfile(models.Model):
    
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
    
    
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_profile")
    date_of_birth=models.DateField(null=True)
    denomination=models.CharField(max_length=20, choices=DenominationChoices.choices, null=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, null=True)
    location=models.CharField(max_length=255, null=True)
    profile_picture=models.ImageField(upload_to='profile-pictures/',  default="profile-pictures/default.jpg", blank=True, null=True)
    bio=models.TextField(blank=True)
    
    @property
    def age(self):
        today=date.today()
        age=today.year -self.date_of_birth.year-((today.month, today.day)< (self.date_of_birth.month, self.date_of_birth.day))
        return age
        
    def __str__(self):
        return f"Profile of {self.user.username}"

    class Meta:
        db_table="user_profiles"