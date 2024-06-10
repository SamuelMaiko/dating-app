from django.dispatch import receiver, Signal
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

cust=Signal()

@receiver(cust, sender=None)
def hand(sender, **kwargs):
    group_name=kwargs["gname"]
    message=kwargs["message"]
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "chat.message",  # Custom event type
            "message": message
        }
    )