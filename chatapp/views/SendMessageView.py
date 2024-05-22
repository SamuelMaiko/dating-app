from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from chatapp.models import Chat, Message
from chatapp.serializers import SendMessageSerializer
from chatapp.permissions import IsChatParticipant
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated, IsChatParticipant]
    
    @swagger_auto_schema(
        operation_description="Sends messages between users and returns the sent messages",
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
                'reply_to': openapi.Schema(type=openapi.TYPE_INTEGER, description='id of the message being replied to'),
            },
            required=['content'],  # Add required fields if any
        ),
        responses={
            201: openapi.Response(
                description="Successful sending oof message",
                examples={
                     "application/json": {
                                "id": 26,
                                "chat": 1,
                                "sender": {
                                    "id": 26,
                                    "username": "ten3"
                                },
                                "content": "Just documenting stuff again",
                                "image": "null",
                                "timestamp": "2024-05-22T18:00:12.104523Z",
                                "reply_to": "null",
                                "is_mine": "true"
 

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
        tags=['Messaging']
    )

    def post(self, request, chat_id):
        try:
            chat = Chat.objects.get(pk=chat_id)
        except Chat.DoesNotExist:
            return Response({"error": "Chat does not exist"}, status=status.HTTP_404_NOT_FOUND)

        request.data["chat"]=chat.id
        
        # Check permissions
        self.check_object_permissions(request, chat)
        
        serializer = SendMessageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Ensure the sender is the logged-in user and associate the message with the chat
            serializer.save(sender=request.user, chat=chat)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)