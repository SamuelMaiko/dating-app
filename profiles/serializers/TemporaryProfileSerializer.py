from rest_framework import serializers
from profiles.models import TemporaryProfile

class TemporaryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryProfile
        fields = ['date_of_birth','gender', 'denomination', 'location', 'profile_picture', 'bio']
