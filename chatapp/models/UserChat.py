from userauth.models import CustomUser
from django.db import models
from .Chat import Chat

class UserChat(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"UserChat {self.user} {self.chat}"
    
    class Meta:
        db_table="user_chats intermediary table"