from django.db import models
from profiles.models import UserProfile, Hobbie

class HobbieProfile(models.Model):
    profile=models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="hobbie_profile")
    hobbie=models.ForeignKey(Hobbie, on_delete=models.CASCADE, related_name="hobbie_profile")

    def __str__(self):
        return f"{self.profile.user.username}'s {self.hobbie.title} hobbie_profile"
    
    class Meta:
        db_table="hobbie_profile"
        unique_together=('profile', 'hobbie')