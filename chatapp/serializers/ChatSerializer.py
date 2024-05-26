from rest_framework import serializers
from .ChatUserSerializer import ChatUserSerializer
from .DetailMessageSerializer import DetailMessageSerializer
from chatapp.models import Chat, Message

class ChatSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_messages_count = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'last_message','unread_messages_count']

    def get_participants(self, obj):
        user = self.context['request'].user
        participants = obj.participants.exclude(id=user.id)
        return ChatUserSerializer(participants, many=True).data
    
    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return DetailMessageSerializer(last_message, context={'request': self.context["request"]}).data
        return None
    
    def get_unread_messages_count(self, obj):
        request = self.context['request']
        unread_messages=Message.objects.filter(chat=obj, is_read=False).exclude(sender=request.user)
        return unread_messages.count()
