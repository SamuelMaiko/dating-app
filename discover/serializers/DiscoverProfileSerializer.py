from rest_framework import serializers
from profiles.models import UserProfile, Favorite

class DiscoverProfileSerializer(serializers.ModelSerializer):
    user_id=serializers.SerializerMethodField(read_only=True)
    username=serializers.SerializerMethodField(read_only=True)
    is_favorite=serializers.SerializerMethodField(read_only=True)
    
    
    class Meta:
        model=UserProfile
        fields=['user_id','username','profile_picture','date_of_birth', "is_favorite"]
        
    def get_username(self, obj):
        return obj.user.username
    
    def get_user_id(self, obj):
        return obj.user.pk
    
    def get_is_favorite(self, obj):
        request=self.context["request"]
        is_favorite=Favorite.objects.filter(user=request.user, favorite=obj.user).exists()
        return is_favorite