from django.contrib import admin
from .models import Message, Chat, UserChat, Block

# Register your models here.
admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(UserChat)
admin.site.register(Block)
