from rest_framework.views import APIView
from profiles.models import UserProfile
from profiles.serializers import ProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from userauth.models import CustomUser
from chatapp.models import Block
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Retrieve a user's profile by passing their id.",
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
                description="Profile retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user'),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the user'),
                        'profile_picture': openapi.Schema(type=openapi.TYPE_STRING, description='URL of the profile picture'),
                        'bio': openapi.Schema(type=openapi.TYPE_STRING, description='Biography of the user'),
                        'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Gender of the user'),
                        'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, description='Date of birth of the user'),
                        'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Age of the user'),
                        'denomination': openapi.Schema(type=openapi.TYPE_STRING, description='Denomination of the user'),
                        'location': openapi.Schema(type=openapi.TYPE_STRING, description='Location of the user'),
                        # Add more properties as needed
                    }
                )
            ),
            403: openapi.Response(
                description="Forbidden if no access token provided",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
        },
        tags=['Profile']
    )
    
    
    def get(self, request, user_id):
        """
        Retrieve the authenticated user's profile details.
        """
        
        try:
            user=CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error":"User with provided id doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        user_profile=user.user_profile
        serializer = ProfileSerializer(user_profile)
        response_data=serializer.data
        
        # adding is_blocked flag
        is_blocked=Block.objects.filter(blocker=user, blocked=request.user).exists()
        response_data["is_blocked"]=is_blocked
        # adding blocked other user flag
        blocked_other_user=Block.objects.filter(blocker=request.user, blocked=user).exists()
        response_data["blocked_other_user"]=blocked_other_user

        return Response(response_data, status=status.HTTP_200_OK)
        
