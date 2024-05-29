from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import UserPhotoSerializer
from userauth.models import CustomUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserPhotosView(APIView):
    permission_classes=[IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Retrieves the photos of the user whose id has been passed.",
    manual_parameters=[
         openapi.Parameter(
                'user_id',
                openapi.IN_PATH,
                description="ID of the user to retrieve their photos",
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
            description="Success",
            examples={
                "application/json": [
                            {
                                "id": 1,
                                "photo": "/media/profile-pictures/wallpaperflare.com_wallpaper.jpg",
                                "created_at": "2024-05-24T05:50:35.200796Z"
                            },
                            {
                                "id": 5,
                                "photo": "/media/user-photos/wallpaperflare.com_wallpaper_3.jpg",
                                "created_at": "2024-05-24T08:12:39.766908Z"
                            }
                        ]
                    }
    
            ),
        404: openapi.Response(
            description="Not found",
            examples={
                "application/json": {
                    "error":"User with id doesn't exist."
                }
                    }
    
            ),
        },
        tags=['Photos']
    )
    
    def get(self, request, user_id):
        try:
            user=CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error":"User with id doesn't exist."}, status=status.HTTP_404_NOT_FOUND)
        
        photos=user.photos.all()
        serializer=UserPhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    