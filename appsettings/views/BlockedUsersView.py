from rest_framework.views import APIView
from appsettings.serializers import BlockedUserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from userauth.models import CustomUser
from chatapp.models import Block
from django.db.models import Subquery
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BlockedUsersView(APIView):
    permission_classes=[IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Retrieves the list of users blocked by the logged in user",
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
            description="Successful retrieval",
            examples={
                "application/json": 
                    [
                        {
                            "id": 6,
                            "username": "sam",
                            "email": "sam@gmail.com"
                        },
                        {
                            "id": 28,
                            "username": "noobie",
                            "email": "noobie@gmail.com"
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
                )
        },
        tags=['Block']
    )
    
    def get(self, request):
        blocked_users_ids=Block.objects.filter(blocker=request.user).values_list('blocked', flat=True)
        blocked_users=CustomUser.objects.filter(id__in=Subquery(blocked_users_ids))
        
        serializer=BlockedUserSerializer(blocked_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)