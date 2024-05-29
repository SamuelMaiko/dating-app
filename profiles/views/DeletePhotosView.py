from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import UserPhotoSerializer
from profiles.permissions import IsPhotoOwner
from profiles.models import UserPhoto
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class DeletePhotosView(APIView):
    permission_classes=[IsAuthenticated, IsPhotoOwner]
    
    @swagger_auto_schema(
    operation_description="Allows the logged user to delete a photo from their photos.",
    manual_parameters=[
         openapi.Parameter(
                'photo_id',
                openapi.IN_PATH,
                description="ID of the photo to delete",
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
        204: openapi.Response(
            description="No content",
            examples={
                "application/json": {
                    "message":"Photo deleted successfully"
                }
                    }
    
            ),
            403: openapi.Response(
                description="Forbidden",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
                ),
            404: openapi.Response(
                description="Not found",
                examples={
                    "application/json": {
                        "error":"Photo with provided id does not exist"
                    }
                }
                ),
        },
        tags=['Photos']
    )

    
    def delete(self, request, photo_id):
        try:
            photo=UserPhoto.objects.get(pk=photo_id)
        except UserPhoto.DoesNotExist:
            return Response({"error":"Photo with provided id does not exist"},  status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, photo)

        photo.delete()
        return Response({"message":"Photo deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    