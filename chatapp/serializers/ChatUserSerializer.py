from rest_framework import serializers
from userauth.models import CustomUser
from .ChatProfileSerializer import ChatProfileSerializer

class ChatUserSerializer(serializers.ModelSerializer):
    user_profile = ChatProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = [ 'username', 'user_profile']