from rest_framework.views import APIView
from profiles.models import UserProfile
from profiles.serializers import ProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Update the authenticated user's profile.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=ProfileSerializer,
        responses={
            200: openapi.Response(
                description="Profile updated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, description='Date of birth of the user'),
                        'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Gender of the user'),
                        'denomination': openapi.Schema(type=openapi.TYPE_STRING, description='Denomination of the user'),
                        'location': openapi.Schema(type=openapi.TYPE_STRING, description='Location of the user'),
                        'profile_picture': openapi.Schema(type=openapi.TYPE_STRING, description='URL of the profile picture'),
                        'bio': openapi.Schema(type=openapi.TYPE_STRING, description='Biography of the user'),
                        # Add more properties as needed
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "Serializer errors"
                    }
                }
            ),
        },
        tags=['Profile']
    )
    
    def put(self, request, format=None):
        
        user_profile=request.user.user_profile

        serializer = ProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
