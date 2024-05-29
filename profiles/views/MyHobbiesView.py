from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import HobbieSerializer
from profiles.models import Hobbie, HobbieProfile, UserProfile
from django.db.models import Subquery
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class MyHobbiesView(APIView):
    permission_classes=[IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Retrieves all the hobbies of the logged user.",
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
        
        # hobbies=user.user_profile.hobbies.all()
        profile=UserProfile.objects.get(user=user)
        hobbies_ids=HobbieProfile.objects.filter(profile=profile).values_list("hobbie", flat=True)
        hobbies=Hobbie.objects.filter(id__in=Subquery(hobbies_ids))
        serializer=HobbieSerializer(hobbies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    