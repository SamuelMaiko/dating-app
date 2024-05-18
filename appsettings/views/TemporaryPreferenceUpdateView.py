from rest_framework.views import APIView
from appsettings.models import TemporaryPreference
from appsettings.serializers import TemporaryPreferenceSerializer
from userauth.models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class TemporaryPreferenceUpdateView(APIView):
    
    @swagger_auto_schema(
        operation_description="Update the temporary preferences of a user using their email.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the user'),
                'min_age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Minimum age preference'),
                'max_age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum age preference'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='Location preference'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Gender preference'),
                'denomination': openapi.Schema(type=openapi.TYPE_STRING, description='Denomination preference'),
                # Add more properties as needed
            },
            required=['email'],  # Add required fields if any
        ),
        responses={
            200: openapi.Response(
                description="Temporary preferences updated successfully",
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
                        "error": "Serializer errors"
                    }
                }
            ),
            404: openapi.Response(
                description="User Not Found",
                examples={
                    "application/json": {
                        "error": "User with provided email does not exist"
                    }
                }
            ),
        },
        tags=['Temporary Preferences']
    )
    
    def put(self, request, format=None):
        email = request.data.get('email')
        
        if not email:
            return Response({"error":"Email not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
            temporary_preference= TemporaryPreference.objects.get(user=user)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with provided email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"T{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TemporaryPreferenceSerializer(temporary_preference, data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # activating the user account
            user.is_active=True
            user.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)