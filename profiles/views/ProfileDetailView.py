from rest_framework.views import APIView
from profiles.models import UserProfile
from profiles.serializers import ProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieve the authenticated user's profile details.",
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
                description="Profile details retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'profile_picture': openapi.Schema(type=openapi.TYPE_STRING, description='URL of the profile picture'),
                        'bio': openapi.Schema(type=openapi.TYPE_STRING, description='Biography of the user'),
                        'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Gender of the user'),
                        'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Age of the user'),
                        'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, description='Date of birth of the user'),
                        'denomination': openapi.Schema(type=openapi.TYPE_STRING, description='Denomination of the user'),
                        'location': openapi.Schema(type=openapi.TYPE_STRING, description='Location of the user'),
                        # Add more properties as needed
                    }
                )
            ),
        },
        tags=['Profile']
    )
    
    
    def get(self, request):
        """
        Retrieve the authenticated user's profile details.
        """
        user_profile=request.user.user_profile
        serializer = ProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
