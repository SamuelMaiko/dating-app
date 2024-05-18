from rest_framework import serializers
from profiles.models import UserProfile

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth','gender', 'denomination', 'location', 'profile_picture', 'bio']
