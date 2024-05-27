from profiles.models import UserProfile
from profiles.serializers import ProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from discover.serializers import DiscoverProfileSerializer
from discover.filters import UserProfileFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class DiscoverView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Shows profiles of other users in the app to discover",
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token token", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('min_age', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Minimum age'),
            openapi.Parameter('max_age', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Maximum age'),
            openapi.Parameter('gender', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Gender'),
            openapi.Parameter('denomination', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Denomination'),
            openapi.Parameter('location', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Location'),
            openapi.Parameter('username', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Username')
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
                            "age": 34
                        },
                        {
                            "user_id": 6,
                            "username": "sam",
                            "profile_picture": "/media/profile-pictures/default.jpg",
                            "date_of_birth": "2010-10-10",
                            "age": 14
                        }
                    ]
                }
            )
        },
        tags=['Discover']
    )
    
    def get(self, request):
        # profiles=UserProfile.objects.all()
        profiles = UserProfile.objects.all()
        filterset = UserProfileFilter(request.GET, queryset=profiles)
        if filterset.is_valid():
            profiles = filterset.qs

        
        serializer=DiscoverProfileSerializer(profiles, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)