from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import HobbieSerializer
from profiles.models import Hobbie, HobbieProfile
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class AddHobbieView(APIView):
    permission_classes=[IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Allows the logged user to add a hobby.",
    manual_parameters=[
        openapi.Parameter(
                'hobbie_id',
                openapi.IN_PATH,
                description="Id of the hobbie the user want to add.",
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
                "application/json": {
                    'message':"Reading added successfully to hobbies."
                }
                    }
    
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        'error':"Cannot add already added hobbie."
                    }
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
                description="Not Found",
                examples={
                    "application/json": {
                        'error':"Hobbie with id doesn't exist"
                    }
                }
                )
        },
        tags=['Hobbies']
    )
    
    def post(self, request, hobbie_id):
        try:
            hobbie=Hobbie.objects.get(pk=hobbie_id)
        except Hobbie.DoesNotExist:
            return Response({'error':"Hobbie with id doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        user_profile=request.user.user_profile
        hobbieprofile=HobbieProfile.objects.filter(profile=user_profile, hobbie=hobbie)

        if hobbieprofile.exists():
            return Response({'error':"Cannot add already added hobbie."}, status=status.HTTP_400_BAD_REQUEST)    
        
        HobbieProfile.objects.create(profile=user_profile, hobbie=hobbie)
        return Response({'message':f"{hobbie.title} added successfully to hobbies."}, status=status.HTTP_200_OK)