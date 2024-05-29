from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from chatapp.models import Chat, Message
from chatapp.permissions import IsChatParticipant
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class MarkMessagesAsReadView(APIView):
    permission_classes = [IsAuthenticated, IsChatParticipant]
    
    @swagger_auto_schema(
    operation_description="Allows logged user to mark messages of a chat as read.",
    manual_parameters=[
        openapi.Parameter(
                'chat_id',
                openapi.IN_PATH,
                description="Id of the chat to be mark messages as read",
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
    responses={
        200: openapi.Response(
            description="Success",
            examples={
                "application/json": {
                    
                    "success": "Messages marked as read"
                }
                    }
    
            ),
            404: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "error": "Chat does not exist"
                    }
                }
                ),
            403: openapi.Response(
                description="Forbidden",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action.",
                        "detail": "Authentication credentials were not provided."
                    }
                }
                )
        },
        tags=['Messaging']
    )

    def post(self, request, chat_id):
        try:
            chat = Chat.objects.get(pk=chat_id)
            
            messages = Message.objects.filter(chat=chat, is_read=False).exclude(sender=request.user)
            
            self.check_object_permissions(request, chat)
            
            messages.update(is_read=True)
            return Response({"success": "Messages marked as read"}, status=status.HTTP_200_OK)
        except Chat.DoesNotExist:
            return Response({"error": "Chat does not exist"}, status=status.HTTP_404_NOT_FOUND)
