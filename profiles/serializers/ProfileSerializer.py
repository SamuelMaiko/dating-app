from rest_framework import serializers
from profiles.models import UserProfile
from profiles.serializers.HobbieSerializer import HobbieSerializer
from datetime import date

class ProfileSerializer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField(read_only=True)
    email=serializers.SerializerMethodField(read_only=True)
    hobbies = HobbieSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['username','email','profile_picture','bio','gender','date_of_birth','age','denomination',  'location','hobbies']
    
    def get_username(self, obj):
        return obj.user.username
    
    def get_email(self, obj):
        return obj.user.email
            