from rest_framework import serializers
from chatapp.models import Chat
from chatapp.serializers import ChatUserSerializer
from .DetailMessageSerializer import DetailMessageSerializer

class DetailChatSerializer(serializers.ModelSerializer):
    # participants = ChatUserSerializer(many=True, read_only=True)
    participants = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'messages', 'created_at']
        
    def get_participants(self, obj):
        user = self.context['request'].user
        participants = obj.participants.exclude(id=user.id)
        return ChatUserSerializer(participants, many=True).data

    def get_messages(self, obj):
        request = self.context.get('request')
        if request and request.user:
            messages = obj.messages.exclude(deleted_by_users=request.user)
            return DetailMessageSerializer(messages, many=True, context={'request': request}).data
        return []