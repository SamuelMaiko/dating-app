from rest_framework import serializers
from .ChatUserSerializer import ChatUserSerializer
from chatapp.models import Message

class MessageSerializer(serializers.ModelSerializer):
    # sender = ChatUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['content', 'timestamp',]
        # fields = ['id', 'chat', 'sender', 'content', 'timestamp', 'deleted_for_sender', 'deleted_for_all']