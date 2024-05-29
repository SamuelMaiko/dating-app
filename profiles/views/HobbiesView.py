from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import HobbieSerializer
from profiles.models import Hobbie, HobbieProfile, UserProfile
from django.db.models import Subquery
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class HobbiesView(APIView):    
    @swagger_auto_schema(
    operation_description="Returns all the hobbies available in the app to choose from.",
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
        },
        tags=['Hobbies']
    )
    
    def get(self, request):
        user=request.user
        # getting logged user hobbies
        profile=UserProfile.objects.get(user=user)
        logged_user_hobbies_ids=HobbieProfile.objects.filter(profile=profile).values_list("hobbie", flat=True)
        
        # removing the logged user hobbies
        hobbies_to_display=Hobbie.objects.exclude(id__in=Subquery(logged_user_hobbies_ids))
        serializer=HobbieSerializer(hobbies_to_display, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    