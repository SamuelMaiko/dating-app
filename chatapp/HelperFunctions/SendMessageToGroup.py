from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

async def send_message_to_group(group_name, message):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        group_name,
        {
            "type": "chat.message",  # Custom event type
            "message": message
        }
    )