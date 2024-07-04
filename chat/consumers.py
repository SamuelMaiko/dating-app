import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from userauth.models import CustomUser
import random

class ChatConsumer(AsyncWebsocketConsumer):

# async def connect(self):

    def get_name(self, message):
        CustomUser.objects.create_user(username=f"{message}{random.randint(0,1000)}", password="lastone447", email=f"{message}{random.randint(0,1000)}@gmail.com")
    def get_token(self, token_key):
        token = Token.objects.get(key=token_key)
        return token
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        # print(self.scope['query_string'].decode().split('=')[1])
        # Authenticate the user using token
        try:
            token_key = self.scope['query_string'].decode().split('=')[1]
            token=database_sync_to_async(self.get_token)(token_key)
            self.scope['user'] = token.user
        except Token.DoesNotExist:
            print("Hello")
            await self.close(code=4003)
            return
        except Exception:
            print("Hello2")
            await self.close(code=4000)
            return

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        if isinstance(message, str):
            message={
                "content":message
            }
        else:
            if int(self.scope["user"]["id"])==message["sender"]["id"]:
                message["is_mine"]=True
            else:
                message["is_mine"]=False
                
        print(self.scope["user"])
        print(message.get("sender") if message.get("sender") else None)
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))
        # self.username = await database_sync_to_async(self.get_name)(message)
        



# import json

# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_{self.room_name}"

#         # Join room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )

#         self.accept()

#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )

#     # Receive message from WebSocket
#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         # Send message to room group
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat.message", "message": message}
#         )

#     # Receive message from room group
#     def chat_message(self, event):
#         message = event["message"]

#         # Send message to WebSocket
#         self.send(text_data=json.dumps({"message": message}))