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
        operation_description="Retrieve details and messages of a specific chat",
        responses={
            200: openapi.Response(
                description="Successful response",
                examples={
                    "application/json": {
    "id": 1,
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
            "id": 7,
            "chat": 3,
            "sender": {
                "id": 26,
                "username": "ten3"
            },
            "content": "Since highschool around form 2",
            "image": "null",
            "timestamp": "2024-05-21T12:21:53.661900Z",
            "deleted_for_user": "false",
            "is_mine": "true",
            "reply_to": {
                "id": 6,
                "chat": 3,
                "sender": {
                    "id": 26,
                    "username": "ten3"
                },
                "content": "WI am a Liverpool fan",
                "image": "null",
                "timestamp": "2024-05-21T12:03:18.008089Z",
                "deleted_for_user": "false",
                "is_mine": "true",
                "reply_to": "null"
            }
        }
    ]
    }
                    }
    
            ),
            404: openapi.Response(
                description="Chat does not exist",
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
        
        