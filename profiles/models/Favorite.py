from django.db import models
from userauth.models import CustomUser

class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, related_name='favorite_user', on_delete=models.CASCADE)
    favorite = models.ForeignKey(CustomUser, related_name='favorited_by_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_favorites'
        unique_together = ('user', 'favorite')

    def __str__(self):
        return f"{self.user.username} favorited {self.favorite.username}"
