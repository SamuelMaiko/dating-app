from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatapp.models import Chat
from chatapp.serializers import DetailChatSerializer
from rest_framework.permissions import IsAuthenticated
from chatapp.permissions import IsChatParticipant
from chatapp.restrictions import can_send_message
from chatapp.models import Block
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ChatDetailsView(APIView):
    permission_classes=[IsAuthenticated, IsChatParticipant]
    
    @swagger_auto_schema(
        operation_description="Retrieves participants,  messages and details of the chat whose id has been provided",
        responses={
            200: openapi.Response(
                description="Successful response",
                examples={
                    "application/json": {
    "id": 1,
    "is_blocked": "false",
    "blocked_other_user": "false",
    "participants": [
        {
            "username": "sam",
            "user_profile": {
                "profile_picture": "/media/profile-pictures/default.jpg",
                "bio": "My profile"
            }
        }
    ],
    "messages": [
        {
            "id": 30,
            "chat": 3,
            "sender": {
                "id": 26,
                "username": "ten3"
            },
            "content": "Wow!, I can actually send a  message with an image",
            "image": "http://localhost:8000/media/message_images/wallpaperflare.com_wallpaper_3.jpg",
            "timestamp": "2024-05-25T13:14:30.787100Z",
            "deleted_for_user": False,
            "is_read": False,
            "is_mine": True,
            "reply_to": None
        },
        {
            "id": 11,
            "chat": 3,
            "sender": {
                "id": 26,
                "username": "ten3"
            },
            "content": "great",
            "image": None,
            "timestamp": "2024-05-21T13:46:36.274737Z",
            "deleted_for_user": False,
            "is_read": False,
            "is_mine": True,
            "reply_to": {
                "id": 10,
                "chat": 3,
                "sender": {
                    "id": 26,
                    "username": "ten3"
                },
                "content": "I can reply to no message, great",
                "image": None,
                "timestamp": "2024-05-21T13:34:29.425785Z",
                "deleted_for_user": False,
                "is_read":False,
                "is_mine": True,
                "reply_to": None
            }
        },
    ]
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
        tags=['Messaging']
    )
    
    def get(self, request, chat_id):
        try:
            chat=Chat.objects.get(pk=chat_id)
        except Chat.DoesNotExist:
            return Response({"error":"Chat does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, chat)

        serializer = DetailChatSerializer(chat, context={'request': request})
        
        response_data=serializer.data        
        # adding is_blocked flag
        other_participant = chat.participants.exclude(id=request.user.id).first()
        is_blocked=Block.objects.filter(blocker=other_participant, blocked=request.user).exists()
        response_data["is_blocked"]=is_blocked
        # adding blocked other user flag
        blocked_other_user=Block.objects.filter(blocker=request.user, blocked=other_participant).exists()
        response_data["blocked_other_user"]=blocked_other_user
        
        return Response(response_data, status=status.HTTP_200_OK)
        
        