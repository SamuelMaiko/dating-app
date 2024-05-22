from rest_framework import serializers
from profiles.models import UserProfile

class DiscoverProfileSerializer(serializers.ModelSerializer):
    user_id=serializers.SerializerMethodField(read_only=True)
    username=serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model=UserProfile
        fields=['user_id','username','profile_picture','date_of_birth']
        
    def get_username(self, obj):
        return obj.user.username
    
    def get_user_id(self, obj):
        return obj.user.pk