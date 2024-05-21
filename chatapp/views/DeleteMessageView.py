from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatapp.models import Message
from chatapp.permissions import IsMessageOwner

class DeleteMessageView(APIView):
    permission_classes = [IsMessageOwner]

    def delete(self, request, message_id):
        try:
            message = Message.objects.get(pk=message_id)
        except Message.DoesNotExist:
            return Response({"error": "Message does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, message)
        message.deleted_by_users.add(request.user)
        message.save()
        
        return Response({"status": "Message deleted"}, status=status.HTTP_200_OK)
