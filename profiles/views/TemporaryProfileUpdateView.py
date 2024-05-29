from rest_framework.views import APIView
from profiles.models import TemporaryProfile
from profiles.serializers import TemporaryProfileSerializer
from userauth.models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class TemporaryProfileUpdateView(APIView):
    
    @swagger_auto_schema(
        operation_description="Update the temporary profile of a user using their email.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the user'),
                'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, description='New date of birth of the user'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='New gender of the user'),
                'denomination': openapi.Schema(type=openapi.TYPE_STRING, description='New denomination of the user'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='New location of the user'),
                'profile_picture': openapi.Schema(type=openapi.TYPE_STRING, description='New URL of the profile picture'),
                'bio': openapi.Schema(type=openapi.TYPE_STRING, description='New biography of the user'),
                # Add more properties as needed
            },
            required=['email'],  # Add required fields if any
        ),
        responses={
            200: openapi.Response(
                description="Temporary profile updated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, description='Date of birth of the user'),
                        'gender': openapi.Schema(type=openapi.TYPE_STRING, description='Gender of the user'),
                        'denomination': openapi.Schema(type=openapi.TYPE_STRING, description='Denomination of the user'),
                        'location': openapi.Schema(type=openapi.TYPE_STRING, description='Location of the user'),
                        'profile_picture': openapi.Schema(type=openapi.TYPE_STRING, description='URL of the profile picture'),
                        'bio': openapi.Schema(type=openapi.TYPE_STRING, description='Biography of the user'),
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
        tags=['Registration']
    )
    
    def put(self, request, format=None):
        email = request.data.get('email')
        
        if not email:
            return Response({"error":"Email not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
            temporary_profile= TemporaryProfile.objects.get(user=user)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with provided email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"T{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TemporaryProfileSerializer(temporary_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)