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
        operation_description="Creates a chat between two users and returns the created chat",
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
                description="Successful creation of chat",
                examples={
                     "application/json": {
                                "id": 4,
                                "participants": [
                                    {
                                        "username": "enock",
                                        "user_profile": "null"
                                    }
                                ],
                                "last_message": "null"
                            }
                }
    
            ),
            404: openapi.Response(
                description="Other user's id not provided",
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
