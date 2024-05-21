from rest_framework import serializers
from profiles.models import UserProfile

class ChatProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture','bio']
 