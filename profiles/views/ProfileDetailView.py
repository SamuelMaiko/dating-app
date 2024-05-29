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
        operation_description="Retrieve the profile of the logged user.",
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
                description="OK",
                examples={
                    "application/json":{
                        "username": "ten3",
                        "email": "samuel.maiko.dev@gmail.com",
                        "profile_picture": "/media/temporary-profile-pictures/default.jpg",
                        "bio": "Just testing stuff.",
                        "gender": "Male",
                        "date_of_birth": "1990-05-15",
                        "age": 34,
                        "denomination": None,
                        "location": "Los Angeles, USA",
                        "hobbies": [
                            {
                                "id": 1,
                                "title": "Dancing"
                            },
                            {
                                "id": 2,
                                "title": "Playing video games"
                            }
                        ]
                    }
                }
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
        
