from django.contrib import admin
from .models import Message, Chat, UserChat

# Register your models here.
admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(UserChat)
