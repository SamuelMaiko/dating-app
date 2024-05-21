from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatapp.models import Chat
from chatapp.serializers import DetailChatSerializer

class ChatDetailsView(APIView):
    def get(self, request, chat_id):
        try:
            chat=Chat.objects.get(pk=chat_id)
        except Chat.DoesNotExist:
            return Response({"error":"Chat does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DetailChatSerializer(chat, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        