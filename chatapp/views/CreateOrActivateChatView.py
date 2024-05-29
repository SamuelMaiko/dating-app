from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatapp.models import Chat, UserChat
from chatapp.serializers import ChatSerializer
from rest_framework.permissions import IsAuthenticated  # Or any other required permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CreateOrActivateChatView(APIView):
    permission_classes = [IsAuthenticated]  # Add appropriate permissions
    
    @swagger_auto_schema(
        operation_description="Creates or activates a chat between two users and returns the created chat",
        manual_parameters=[
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
                'other_user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id of the user to start a new chat with'),
            },
            required=['other_user_id'],  # Add required fields if any
        ),
        responses={
            201: openapi.Response(
                description="Created",
                examples={
                     "application/json": {
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
                        "error": "Other user ID is required"
                    }
                }
                )
        },
        tags=['Messaging']
    )

    def post(self, request):
        # Get the user ID of the other user from the request data
        other_user_id = request.data.get('other_user_id')
        if not other_user_id:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # Get the current user
        current_user = request.user

        # Check if an association between the current user and the other user already exists
        association = UserChat.objects.filter(user=current_user, chat__participants=other_user_id).first()

        if association:
            # If association exists, mark it as not deleted
            association.deleted = False
            association.save()
            chat = association.chat
        else:
            # If association doesn't exist, create a new chat and associate the users with it
            chat = Chat.objects.create()
            chat.participants.add(current_user, other_user_id)
        
        # Serialize the chat and return it in the response
        serializer = ChatSerializer(chat, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
