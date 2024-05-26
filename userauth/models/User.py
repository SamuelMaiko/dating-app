from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    favorites = models.ManyToManyField('self', symmetrical=False, related_name='favorited_by', blank=True)
    blockers = models.ManyToManyField(
        'self',
        through='chatapp.Block',
        related_name='blocked_users',
        symmetrical=False,
        blank=True
    )
    is_verified=models.BooleanField(default=False)
    transfer_completed=models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table="users" 
        verbose_name_plural="Users"
        
    