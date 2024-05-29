from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import UserPhotoSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class MyPhotosView(APIView):
    permission_classes=[IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Retrieves the photos of the logged user.",
    manual_parameters=[
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
            403: openapi.Response(
                description="Forbidden",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
                ),
        },
        tags=['Photos']
    )
    
    def get(self, request):
        user=request.user
        
        photos=user.photos.all()
        serializer=UserPhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    