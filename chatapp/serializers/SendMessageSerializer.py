from rest_framework import serializers
from chatapp.models import Message
from .DetailMessageSerializer import DetailMessageSerializer

class SendMessageSerializer(serializers.ModelSerializer): 
    reply_to = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), required=False, allow_null=True)
    is_mine=serializers.SerializerMethodField()
    image = serializers.ImageField(required=False)
    content = serializers.CharField(required=False)
    
    class Meta:
        model = Message 
        fields = ['id', 'chat', 'sender', 'content','image', 'timestamp','reply_to', 'is_mine']
        read_only_fields = ['id', 'sender', 'timestamp']

    def to_representation(self, instance):
        """ Convert `reply_to` to a nested representation. """
        ret = super().to_representation(instance)
        ret['reply_to'] = DetailMessageSerializer(instance.reply_to, context=self.context).data if instance.reply_to else None
        ret['sender'] = {"id": instance.sender.id, "username": instance.sender.username}
        return ret
    
    def get_is_mine(self, obj):
        request = self.context.get('request')
        logged_in_user=request.user
        
        return obj.sender==logged_in_user
