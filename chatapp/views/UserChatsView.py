from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from chatapp.models import UserChat
from chatapp.serializers import ChatSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UserChatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieves the chats of the logged user",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Successful retrieval of chats",
                examples={
                     "application/json": [
                {
                    "id": 1,
                    "participants": [
                        {
                            "id": 6,
                            "username": "sam",
                            "user_profile": {
                                "profile_picture": "/media/profile-pictures/default.jpg",
                                "bio": "My profile"
                            }
                        }
                    ],
                    "last_message": {
                        "id": 31,
                        "chat": 1,
                        "sender": {
                            "id": 26,
                            "username": "ten3"
                        },
                        "content": "You can see this message but can't reply",
                        "image": "http://localhost:8000/media/message_images/wallpaperflare.com_wallpaper_3_n1rxgDd.jpg",
                        "timestamp": "2024-05-26T10:08:23.806265Z",
                        "deleted_for_user": False,
                        "is_read": False,
                        "is_mine": True,
                        "reply_to": None
                    },
                    "unread_messages_count": 0
                },
                {
                    "id": 3,
                    "participants": [
                        {
                            "id": 28,
                            "username": "noobie",
                            "user_profile": {
                                "profile_picture": "/media/profile-pictures/wallpaperflare.com_wallpaper_1_pOS7bAj.jpg",
                                "bio": "First lady of the platform"
                            }
                        }
                    ],
                    "last_message": {
                        "id": 32,
                        "chat": 3,
                        "sender": {
                            "id": 26,
                            "username": "ten3"
                        },
                        "content": "Hello documenting the APIs",
                        "image": None,
                        "timestamp": "2024-05-29T21:05:25.780520Z",
                        "deleted_for_user": False,
                        "is_read": False,
                        "is_mine": True,
                        "reply_to": None
                    },
                    "unread_messages_count": 0
                }
            ]
                }
    
            ),
             403: openapi.Response(
                description="Forbidden",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            )
        },
        tags=['Messaging']
    )

    def get(self, request):
        user = request.user
        user_chats = UserChat.objects.filter(user=user, deleted=False)
        chats = [user_chat.chat for user_chat in user_chats]
        serializer = ChatSerializer(chats, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
