from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatapp.models import Chat, UserChat
from chatapp.serializers import ChatSerializer
from rest_framework.permissions import IsAuthenticated  # Or any other required permissions

class CreateOrActivateChatView(APIView):
    permission_classes = [IsAuthenticated]  # Add appropriate permissions

    def post(self, request):
        # Get the user ID of the other user from the request data
        other_user_id = request.data.get('other_user_id')
        if not other_user_id:
            return Response({"error": "Other user ID is required"}, status=status.HTTP_400_BAD_REQUEST)

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
