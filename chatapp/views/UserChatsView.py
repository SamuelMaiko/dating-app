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
        operation_description="Retrieves the list of chats of the current logged in user",
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
                                                "username": "sam",
                                                "user_profile": {
                                                    "profile_picture": "/media/profile-pictures/default.jpg",
                                                    "bio": "My profile"
                                                }
                                            }
                                        ],
                                        "last_message": {
                                            "id": 26,
                                            "chat": 1,
                                            "sender": {
                                                "id": 26,
                                                "username": "ten3"
                                            },
                                            "content": "Just documenting stuff again",
                                            "image": "null",
                                            "timestamp": "2024-05-22T18:00:12.104523Z",
                                            "deleted_for_user": "false",
                                            "is_mine": "true",
                                            "reply_to": "null"
                                        }
                                    },
                                    {
                                        "another chat":""
                                    },
                                    {
                                        "another chat":""
                                    },
                                    ]
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
