from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatapp.models import Chat, UserChat
from chatapp.permissions import IsChatParticipant
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class DeleteChatView(APIView):
    permission_classes = [IsChatParticipant]  # Optional: Use a custom permission if needed

    @swagger_auto_schema(
        operation_description="Deletes the chat from the records of a single user",
        manual_parameters=[
            openapi.Parameter(
                'chat_id',
                openapi.IN_PATH,
                description="ID of the chat to delete",
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
                description="Successful removal of chat from user's records",
                examples={
                     "application/json": {
                         "status": "Chat deleted for user"
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
                ),
            403: openapi.Response(
                description="Chat not associated to the logged user",
                examples={
                    "application/json": {
                        "error": "User is not associated with this chat"
                    }
                }
                )
        },
        tags=['Messaging']
    )

    def delete(self, request, chat_id):
        try:
            chat = Chat.objects.get(pk=chat_id)
        except Chat.DoesNotExist:
            return Response({"error": "Chat does not exist"}, status=status.HTTP_404_NOT_FOUND)

        # Optional: Check permissions
        self.check_object_permissions(request, chat)

        # Mark the chat as deleted
        user_chat = UserChat.objects.filter(user=request.user, chat=chat).first()
        if user_chat:
            user_chat.deleted = True
            user_chat.save()
        else:
            # Handle case where user is not associated with the chat
            return Response({"error": "User is not associated with this chat"}, status=status.HTTP_403_FORBIDDEN)

        # Clear the record of messages by adding the user to deleted_for_everyone for each message
        messages = chat.messages.all()
        current_user = request.user
        for message in messages:
            message.deleted_by_users.add(current_user)

        return Response({"status": "Chat deleted for user"}, status=status.HTTP_200_OK)
