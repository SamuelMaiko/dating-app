from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from chatapp.models import Chat, Message
from chatapp.serializers import SendMessageSerializer
from chatapp.permissions import IsChatParticipant

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated, IsChatParticipant]

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