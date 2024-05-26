from django.contrib import admin
from .models import UserProfile, TemporaryProfile, UserPhoto, Favorite, Hobbie, HobbieProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(TemporaryProfile)
admin.site.register(UserPhoto)
admin.site.register(Favorite)
admin.site.register(Hobbie)
admin.site.register(HobbieProfile)