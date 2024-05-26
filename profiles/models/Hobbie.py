from django.db import models
from profiles.models import UserProfile
from django.utils import timezone

class Hobbie(models.Model):
    profiles=models.ManyToManyField(UserProfile, related_name="hobbies", through="HobbieProfile", blank=True)
    title=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=timezone.now())

    def __str__(self):
        return self.title
    
    class Meta:
        db_table="hobbies"
    
    