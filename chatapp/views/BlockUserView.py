from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from chatapp.models import Block
from userauth.models import CustomUser
from django.shortcuts import get_object_or_404
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BlockUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Allows the logged user to block another user.",
    manual_parameters=[
        openapi.Parameter(
                'user_id',
                openapi.IN_PATH,
                description="Id of the user to be blocked",
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
        201: openapi.Response(
            description="Success",
            examples={
                "application/json": {
                    
                    "message": "User blocked successfully"
                }
                    }
    
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "error": "User with id not found",
                        "error": "You cannot block yourself"
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
                )
        },
        tags=['Block']
    )

    def post(self, request, user_id):
        try:
            user_to_block = get_object_or_404(CustomUser, pk=user_id)
        except Http404:
            return Response({"error": "User with id not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user==user_to_block:
            return Response({"error": "You cannot block yourself"}, status=status.HTTP_400_BAD_REQUEST)
            
        
        Block.objects.get_or_create(blocker=request.user, blocked=user_to_block)
        return Response({"message": "User blocked successfully"}, status=status.HTTP_201_CREATED)
