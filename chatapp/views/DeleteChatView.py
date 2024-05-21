from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatapp.models import Chat, UserChat
from chatapp.permissions import IsChatParticipant

class DeleteChatView(APIView):
    permission_classes = [IsChatParticipant]  # Optional: Use a custom permission if needed

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
            return Response({"error": "User is not associated with this chat"}, status=status.HTTP_404_NOT_FOUND)

        # Clear the record of messages by adding the user to deleted_for_everyone for each message
        messages = chat.messages.all()
        current_user = request.user
        for message in messages:
            message.deleted_by_users.add(current_user)

        return Response({"status": "Chat deleted for user"}, status=status.HTTP_200_OK)
