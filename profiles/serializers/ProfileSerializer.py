from rest_framework import serializers
from profiles.models import UserProfile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture','bio','gender','age','date_of_birth','denomination',  'location' ]
