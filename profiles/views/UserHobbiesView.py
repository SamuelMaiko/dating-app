from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import HobbieSerializer
from userauth.models import CustomUser
from profiles.models import Hobbie, HobbieProfile, UserProfile
from django.db.models import Subquery
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserHobbiesView(APIView):
    permission_classes=[IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Retrieves the hobbies of the user whose id has been passed.",
    manual_parameters=[
         openapi.Parameter(
                'user_id',
                openapi.IN_PATH,
                description="ID of the user to retrieve their hobbies",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
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
                                "id": 3,
                                "title": "Reading"
                            },
                            {
                                "id": 4,
                                "title": "Watching movies"
                            }
                        ]
                    }
    
            ),
        404: openapi.Response(
            description="Not found",
            examples={
                "application/json": {
                    "error":"User with id doesn't exist."
                }
                    }
    
            ),
        },
        tags=['Hobbies']
    )
    
    def get(self, request, user_id):
        try:
            user=CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error":"User with id doesn't exist."}, status=status.HTTP_404_NOT_FOUND)
        
        profile=UserProfile.objects.get(user=user)
        hobbies_ids=HobbieProfile.objects.filter(profile=profile).values_list("hobbie", flat=True)
        hobbies=Hobbie.objects.filter(id__in=Subquery(hobbies_ids))
        serializer=HobbieSerializer(hobbies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    