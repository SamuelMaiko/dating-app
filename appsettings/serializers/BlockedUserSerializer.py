from rest_framework import serializers
from userauth.models import CustomUser

class BlockedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['id', "username", "email"]