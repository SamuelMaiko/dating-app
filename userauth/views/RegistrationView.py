from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from userauth.models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from userauth.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from userauth.HelperFunctions import SendWelcomeEmail, SendAccountActivationEmail
from userauth.HelperFunctions import create_otp_model
from userauth.signals import send_otp_signal
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




class RegistrationView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_description="Register a new user and receive OTP to verify email.",
        request_body=UserSerializer,
        responses={
            201: openapi.Response(
                description="Registration successful and OTP sent",
                examples={
                    "application/json": {
                        "message": "registration successful",
                        "success": True
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": {
                            "username": [
                                "This field is required."
                            ],
                            "email": [
                                "This field is required."
                            ],
                            # other possible errors
                        },
                        "success": False
                    }
                }
            ),
        },
        tags=['Registration']
    )

    def post(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            data=serializer.validated_data
            data['is_active']=False
            user=serializer.save()

            # create OTP model for user
            create_otp_model(user)
            # sending otp
            send_otp_signal.send(sender=None,user=user)
            
            return Response({"message":"registration successful, OTP sent.", "success":True}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors,"success":False}, status=status.HTTP_400_BAD_REQUEST)