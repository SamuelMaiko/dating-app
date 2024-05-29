from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import HobbieSerializer
from profiles.models import Hobbie, HobbieProfile, UserProfile
from django.db.models import Subquery
from appsettings.models import Preference
from django.shortcuts import get_object_or_404
from django.http import Http404
from profiles.models import UserProfile
from discover.serializers import DiscoverProfileSerializer
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class MyMatchesView(APIView):
    permission_classes=[IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Retrieves the matches of the logged user.",
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
                                "user_id": 28,
                                "username": "noobie",
                                "profile_picture": "http://localhost:8000/media/profile-pictures/wallpaperflare.com_wallpaper_1_pOS7bAj.jpg",
                                "date_of_birth": "2004-06-12",
                                "age": 19,
                                "is_favorite": "false"
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
            404: openapi.Response(
                description="Not found - user has no preferences set (needed to find match)",
                examples={
                    "application/json": {
                        "error": "No preferences for the user found"
                    }
                }
                ),
        },
        tags=['Match']
    )


    def get(self, request):
        user=request.user
        # get user preferences
        try:
            preference=get_object_or_404(Preference, user=user)
        except Http404:
            return Response({"error": "No preferences for the user found"}, status=status.HTTP_404_NOT_FOUND)

        # get all user profiles except theirs
        profiles = UserProfile.objects.exclude(user=user)
        
        # filter them depending on all the preferences
        # Get today's date
        today = timezone.now().date()

        # Calculate min and max birthdate based on min_age and max_age
        max_birthdate = today.replace(year=today.year - preference.min_age)
        min_birthdate = today.replace(year=today.year - preference.max_age)

        # Filter user profiles based on preferences

        # Applying age filter
        profiles = profiles.filter(date_of_birth__range=(min_birthdate, max_birthdate))

        # Applying gender filter if specified
        if preference.gender:
            profiles = profiles.filter(gender=preference.gender)

        # Applying denomination filter if specified
        if preference.denomination:
            profiles = profiles.filter(denomination=preference.denomination)

        # Applying location filter if specified
        if preference.location:
            profiles = profiles.filter(location__icontains=preference.location)

        # Serialize the filtered profiles
        serializer = DiscoverProfileSerializer(profiles, many=True, context={'request': request})

        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    