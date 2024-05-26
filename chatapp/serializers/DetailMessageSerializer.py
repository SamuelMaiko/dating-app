from rest_framework import serializers
from chatapp.models import Message
from chatapp.serializers.SenderSerializer import SenderSerializer

class DetailMessageSerializer(serializers.ModelSerializer):
    sender = SenderSerializer(read_only=True)
    deleted_for_user = serializers.SerializerMethodField()
    is_mine=serializers.SerializerMethodField()
    content=serializers.SerializerMethodField()
    reply_to = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False)
    
    
    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'content', 'image','timestamp','deleted_for_user','is_read','is_mine','reply_to']

    def get_deleted_for_user(self, obj):
        request = self.context.get('request')
        if request and request.user:
            if obj.sender == request.user:
                return obj.deleted_for_sender
            else:
                return obj.deleted_for_all
    
    def get_is_mine(self, obj):
        request = self.context.get('request')
        logged_in_user=request.user
        
        return obj.sender==logged_in_user
    
    def get_content(self,obj):
        # if obj.deleted_for_all:
        #     return "This message has been deleted"
            
        if obj.deleted_for_all or self.get_deleted_for_user(obj):
            return "This message has been deleted"
        return obj.content
    
    def get_reply_to(self, obj):
        if obj.reply_to:
            return DetailMessageSerializer(obj.reply_to, context=self.context).data
        return None
    
