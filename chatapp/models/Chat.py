from userauth.models import CustomUser
from django.db import models
from django.utils import timezone

class Chat(models.Model):
    participants = models.ManyToManyField(CustomUser, through='UserChat')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Chat {self.pk}"
    
    class Meta:
        db_table="chats"