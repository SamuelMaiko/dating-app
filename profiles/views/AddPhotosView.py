from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import UserPhotoSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class AddPhotosView(APIView):
    permission_classes=[IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Allows the logged user to add a photo to their list of photos.",
    request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'photo': openapi.Schema(type=openapi.TYPE_STRING, description='File of the image to be added'),
            },
            required=['photo']
        ),
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
        201: openapi.Response(
            description="Success",
            examples={
                "application/json": {
                        "id": 8,
                        "photo": "/media/user-photos/wallpaperflare.com_wallpaper_3_WtBXj1I.jpg",
                        "created_at": "2024-05-29T20:36:34.665752Z"
                    }
                    }
    
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "error": "photo is required"
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
        },
        tags=['Photos']
    )
    
    def post(self, request):
        if not request.data.get("photo"):
            return Response({"error":"photo is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = UserPhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    