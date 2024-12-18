from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from chatapp.models import Chat, Message
from chatapp.serializers import SendMessageSerializer
from chatapp.permissions import IsChatParticipant
from chatapp.restrictions import can_send_message
from chatapp.models import Block
from chatapp.HelperFunctions import send_message_to_group
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from chatapp.consumers import ChatConsumer
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated, IsChatParticipant]
    
    @swagger_auto_schema(
        operation_description="Sends messages between users in a chat and returns the sent message",
        manual_parameters=[
            openapi.Parameter(
                'chat_id',
                openapi.IN_PATH,
                description="ID of the chat to retrieve",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'content': openapi.Schema(type=openapi.TYPE_STRING, description='content of the message being sent'),
                'image': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY, description='Image file to be sent with the message'),
                'reply_to': openapi.Schema(type=openapi.TYPE_INTEGER, description='id of the message being replied to'),
            },
            required=['content'],  # Add required fields if any
        ),
        responses={
            201: openapi.Response(
                description="Created",
                examples={
                     "application/json": {
                                "id": 32,
                                "chat": 3,
                                "sender": {
                                    "id": 26,
                                    "username": "ten3"
                                },
                                "content": "Hello documenting the APIs",
                                "image": None,
                                "timestamp": "2024-05-29T21:05:25.780520Z",
                                "reply_to": None,
                                "is_mine": True
                            }
                }
    
            ),
            403: openapi.Response(
                description="Forbidden",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
            404: openapi.Response(
                description="Not found",
                examples={
                    "application/json": {
                        "error":"Chat does not exist"
                    }
                }
            )
        },
        tags=['Messaging']
    )

    
    def post(self, request, chat_id):
        try:
            chat = Chat.objects.get(pk=chat_id)
        except Chat.DoesNotExist:
            return Response({"error": "Chat does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # request.data["chat"]=chat.id
        
        # Check permissions
        self.check_object_permissions(request, chat)

        # handling where user has blocked the other user
        other_participant = chat.participants.exclude(id=request.user.id).first()
        blocked_other_user=Block.objects.filter(blocker=request.user, blocked=other_participant).exists()
        if blocked_other_user:
            return Response({"error":"You have blocked the user. You cannot send messages to this user"}, status=status.HTTP_403_FORBIDDEN)
        
        # handling where user has been blocked
        other_user=chat.participants.exclude(id=request.user.id).first()
        if not can_send_message(request.user, other_user):
            return Response({"error":"You are blocked. You cannot send messages to this user"}, status=status.HTTP_403_FORBIDDEN)
        data=request.data.copy()
        data["chat"]=chat.id
        serializer = SendMessageSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            # Ensure the sender is the logged-in user and associate the message with the chat
            serializer.save(sender=request.user, chat=chat)
            
            channel_layer = get_channel_layer()
        
            async_to_sync(channel_layer.group_send)(
                "chat_NY",
                {
                    "type": "chat.message",
                    "message": {
                        "id":serializer.data["id"],
                        "content":serializer.data["content"],
                        "sender":serializer.data["sender"],
                        'image':serializer.data["image"],
                        "timestamp":serializer.data["timestamp"],
                        "reply_to":serializer.data["reply_to"]
                    }
                }
            )
            print("Woow")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)