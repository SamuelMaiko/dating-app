from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from userauth.models import CustomUser
from profiles.models import HobbieProfile, Hobbie
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RemoveHobbieView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Allows the logged user to remove a hobby from their list.",
    manual_parameters=[
        openapi.Parameter(
                'hobbie_id',
                openapi.IN_PATH,
                description="Id of the hobby to remove.",
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
        204: openapi.Response(
            description="No content",
            examples={
                "application/json": {
                    "message": "Reading removed successfully from hobbies."
                }
                    }
    
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        'error':"Cannot remove a hobbie you don't have."
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
                description="Not found",
                examples={
                    "application/json": {
                        'error':"Hobbie with id doesn't exist"
                    }
                }
                ),
        },
        tags=['Hobbies']
    )


    def delete(self, request, hobbie_id):
        try:
            hobbie=Hobbie.objects.get(pk=hobbie_id)
        except Hobbie.DoesNotExist:
            return Response({'error':"Hobbie with id doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        profile=request.user.user_profile
        hobbieProfile=HobbieProfile.objects.filter(profile=profile, hobbie=hobbie)

        if not hobbieProfile.exists():
            return Response({'error':"Cannot remove a hobbie you don't have."}, status=status.HTTP_400_BAD_REQUEST) 
        
        hobbieProfile.delete()
        return Response({'message':f"{hobbie.title} removed successfully from hobbies."}, status=status.HTTP_204_NO_CONTENT)
        