from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chatapp.models import Message
from chatapp.permissions import IsMessageOwner
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class DeleteMessageForEveryoneView(APIView):
    permission_classes = [IsMessageOwner]

    @swagger_auto_schema(
        operation_description="Deletes a message for all the partcipants of the chat",
        manual_parameters=[
            openapi.Parameter(
                'message_id',
                openapi.IN_PATH,
                description="id of the message to be deleted",
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
                description="Successful deletion of the message",
                examples={
                     "application/json": {
                        "status": "Message deleted for everyone"
                    }
                }
    
            ),
            403: openapi.Response(
                description="Can't delete a message not belonging to you",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action."
                    }
                }
                ),
            404: openapi.Response(
                description="Message does not exist",
                examples={
                    "application/json": {
                        "error": "Message does not exist"
                    }
                }
                )
        },
        tags=['Messaging']
    )
    
    def delete(self, request, message_id):
        try:
            message = Message.objects.get(pk=message_id)
        except Message.DoesNotExist:
            return Response({"error": "Message does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, message)
        message.deleted_for_all = True
        message.save()
        
        return Response({"status": "Message deleted for everyone"}, status=status.HTTP_200_OK)
