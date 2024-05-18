from django.contrib import admin
from .models import Preference, TemporaryPreference

# Register your models here.
admin.site.register(Preference)
admin.site.register(TemporaryPreference)