from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from chatapp.models import UserChat
from chatapp.serializers import ChatSerializer

class UserChatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_chats = UserChat.objects.filter(user=user, deleted=False)
        chats = [user_chat.chat for user_chat in user_chats]
        serializer = ChatSerializer(chats, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
