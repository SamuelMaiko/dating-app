from rest_framework import serializers
from profiles.models import Favorite
from userauth.models import CustomUser

class FavoriteSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='favorite', queryset=CustomUser.objects.all())
    username = serializers.ReadOnlyField(source='favorite.username')
    profile_picture = serializers.SerializerMethodField()
    date_of_birth = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ['user_id', 'username', 'profile_picture','age', 'date_of_birth']

    def get_profile_picture(self, obj):
        return obj.favorite.user_profile.profile_picture.url if obj.user.user_profile.profile_picture else None

    def get_date_of_birth(self, obj):
        return obj.favorite.user_profile.date_of_birth if obj.user.user_profile.date_of_birth else None
    
    def get_age(self, obj):
        return obj.favorite.user_profile.age if obj.user.user_profile.date_of_birth else None
