from django.db import models
from userauth.models import CustomUser

class Block(models.Model):
    blocker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocker')
    blocked = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocked')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked')
        db_table = "user_blocks"

    def __str__(self):
        return f"{self.blocker.username} blocked {self.blocked.username}"
