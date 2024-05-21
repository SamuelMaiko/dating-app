from rest_framework import serializers
from userauth.models import CustomUser

class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']