from django.contrib import admin
from .models import UserProfile, TemporaryProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(TemporaryProfile)