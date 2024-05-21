from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatapp.models import Message
from chatapp.permissions import IsMessageOwner

class DeleteMessageForEveryoneView(APIView):
    permission_classes = [IsMessageOwner]

    # def permission_denied(self, request, message=None, code=None):
    #     if request.authenticators and not request.successful_authenticator:
    #         raise exceptions.NotAuthenticated()
    #     raise exceptions.PermissionDenied(detail="You do not have permission to delete this message for everyone.")

    def delete(self, request, message_id):
        try:
            message = Message.objects.get(pk=message_id)
        except Message.DoesNotExist:
            return Response({"error": "Message does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, message)
        message.deleted_for_all = True
        message.save()
        
        return Response({"status": "Message deleted for everyone"}, status=status.HTTP_200_OK)
