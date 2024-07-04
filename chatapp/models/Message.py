from userauth.models import CustomUser
from django.db import models
from django.utils import timezone
from .Chat import Chat

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(default="")
    image = models.ImageField(upload_to='message_images/', null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    deleted_for_sender = models.BooleanField(default=False)
    deleted_for_all = models.BooleanField(default=False)
    deleted_by_users = models.ManyToManyField(CustomUser, related_name='deleted_messages', blank=True)
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='replies')

    
    def __str__(self):
        return f"{self.content} from {self.sender.username}"
    
    class Meta:
        db_table="messages"