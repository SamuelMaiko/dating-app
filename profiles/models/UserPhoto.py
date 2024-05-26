from django.db import models
from userauth.models import CustomUser

class UserPhoto(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="photos")
    photo=models.ImageField(upload_to='user-photos/', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s photo id {self.id}"

    class Meta:
        db_table="user_photos"