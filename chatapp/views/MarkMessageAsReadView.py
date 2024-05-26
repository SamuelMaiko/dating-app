from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from chatapp.models import Chat, Message
from chatapp.permissions import IsChatParticipant

class MarkMessagesAsReadView(APIView):
    permission_classes = [IsAuthenticated, IsChatParticipant]

    def post(self, request, chat_id):
        try:
            chat = Chat.objects.get(pk=chat_id)
            
            messages = Message.objects.filter(chat=chat, is_read=False).exclude(sender=request.user)
            
            self.check_object_permissions(request, chat)
            
            messages.update(is_read=True)
            return Response({"success": "Messages marked as read"}, status=status.HTTP_200_OK)
        except Chat.DoesNotExist:
            return Response({"error": "Chat does not exist"}, status=status.HTTP_404_NOT_FOUND)
