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
        operation_description="Retrieve the profile of the user id passed.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token token",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'user_id',
                openapi.IN_PATH,
                description="ID of the user to retrieve profile",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Profile retrieved successfully",
                examples={
                    "application/json":{
                        "username": "sam",
                        "email": "sam@gmail.com",
                        "profile_picture": "/media/profile-pictures/default.jpg",
                        "bio": "My profile",
                        "gender": "Male",
                        "date_of_birth": "2020-10-10",
                        "age": 3,
                        "denomination": "Protestant",
                        "location": "Nairobi, Kenya",
                        "hobbies": [
                            {
                                "id": 2,
                                "title": "Playing video games"
                            }
                        ],
                        "is_blocked": False,
                        "blocked_other_user": True
                    }
                }
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
        
