from rest_framework.views import APIView
from appsettings.serializers import PreferenceSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PreferenceUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Update the authenticated user's preferences.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=PreferenceSerializer,
        responses={
            200: openapi.Response(
                description="Preferences updated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'min_age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Minimum age preference'),
                        'max_age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum age preference'),
                        'location': openapi.Schema(type=openapi.TYPE_STRING, description='Location preference'),
                        'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Gender preference'),
                        'denomination': openapi.Schema(type=openapi.TYPE_STRING, description='Denomination preference'),
                        # Add more properties as needed
                    }
                )
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "serializer errors"
                    }
                }
            ),
        },
        tags=['Preferences']
    )
    
    def put(self, request, format=None):
        
        user_preference=request.user.preference

        serializer = PreferenceSerializer(user_preference, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
