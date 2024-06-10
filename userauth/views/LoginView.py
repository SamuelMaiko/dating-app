from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from userauth.models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from userauth.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from django.conf import settings
from userauth.signals import (
    transfer_profile_data_signal,
    transfer_preference_data_signal
    )
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class LoginView(APIView):
    permission_classes = [AllowAny]
     
    @swagger_auto_schema(
        operation_description="Login with username and password to obtain authentication token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Successful login",
                examples={
                    "application/json": {
                        "user": {
                            "username": "user1",
                            "email": "user1@example.com",
                            "first_name": "First",
                            "last_name": "Last"
                        },
                        "token": "abc123"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "Provide username password."
                    }
                }
            ),
            404: openapi.Response(
                description="Invalid credentials",
                examples={
                    "application/json": {
                        "error": "Invalid username or password"
                    }
                }
            ),
        },
        tags=['Authentication']
    )
    
    def post(self, request):
        username=request.data.get('username')
        password=request.data.get('password')
        
        message='Provide '
        if not username:
            message+="username "
        
        if not password:
            # message+=message=="Provide "?"":""
            message+="password."
        if message !="Provide ":
            return Response({"error":message}, status=status.HTTP_400_BAD_REQUEST)
        
        
        user=authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # getting user token 
            token, created_token=Token.objects.get_or_create(user=user)
            user_instance=get_object_or_404(CustomUser, username=username)
            serializer=UserSerializer(user_instance)
            
            response_dict={
                "user":serializer.data,
                "token":token.key
                }
                
            return Response(response_dict, status=status.HTTP_200_OK)
        # If user returns NONE = wrong credentials
        else:
            # print(get_object_or_404(CustomUser, email=email).password)
            response_dict={"error": "Invalid username or password"}
            return Response(response_dict, status=status.HTTP_404_NOT_FOUND)
