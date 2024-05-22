from profiles.models import UserProfile
from profiles.serializers import ProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from discover.serializers import DiscoverProfileSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class DiscoverView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Shows profiles of other users in the app to discover",
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
                description="Successful retrieval of profiles",
                examples={
                     "application/json": [
                            {
                                "user_id": 26,
                                "username": "ten3",
                                "profile_picture": "/media/temporary-profile-pictures/default.jpg",
                                "date_of_birth": "1990-05-15",
                                "age":34
                            },
                            {
                                "user_id": 6,
                                "username": "sam",
                                "profile_picture": "/media/profile-pictures/default.jpg",
                                "date_of_birth": "2010-10-10",
                                "age":14
                            }
                        ]
                }
    
            )
        },
        tags=['Discover']
    )
    
    def get(self, request):
        profiles=UserProfile.objects.all()
        
        serializer=DiscoverProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)