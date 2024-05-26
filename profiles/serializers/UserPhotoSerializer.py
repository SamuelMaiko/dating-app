from rest_framework import serializers
from profiles.models import UserPhoto

class UserPhotoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=UserPhoto
        fields=['id','photo', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']