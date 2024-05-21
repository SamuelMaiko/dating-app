from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    is_verified=models.BooleanField(default=False)
    transfer_completed=models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table="users" 
        verbose_name_plural="Users"
        
    