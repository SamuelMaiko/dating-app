from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from userauth.models import CustomUser, EmailOTP
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class VerifyOTPView(APIView):
    
    @swagger_auto_schema(
        operation_description="Verify the OTP sent to the user's email.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the user'),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='OTP sent to the user\'s email'),
            },
            required=['email', 'otp']
        ),
        responses={
            200: openapi.Response(
                description="OTP verification successful",
                examples={
                    "application/json": {
                        "temp_token": "temporary_token",
                        "message": "OTP verification successful.",
                        "success": True
                    }
                }
            ),
            400: openapi.Response(
                description="Expired OTP",
                examples={
                    "application/json": {
                        "message": "OTP has expired. Request for new one."
                    }
                }
            ),
            404: openapi.Response(
                description="Invalid OTP",
                examples={
                    "application/json": {
                        "error": "Email not provided"
                    },
                    "application/json": {
                        "error": "OTP not provided"
                    },
                    "application/json": {
                        "error": "User with email doesn't exist"
                    },
                    "application/json": {
                        "message": "OTP has expired. Request for new one."
                    },
                    "application/json": {
                        "error": "Invalid OTP provided"
                    }
                }
            ),
        },
        tags=['Authentication']
    )
    
    def post(self, request):
        email=request.data.get("email")
        user_entered_otp=request.data.get("otp")
        
        if not email:
            return Response({"error":"Email not provided"}, status=status.HTTP_400_BAD_REQUEST)
        if not user_entered_otp:
            return Response({"error":"OTP not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        user=CustomUser.objects.filter(email=email).first()
        
        if not user:
            return Response({"error":"user with email doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        email_otp=EmailOTP.objects.get(user=user)
        
        # if otp matches 
        if email_otp.otp==user_entered_otp:
            # if otp not expired
            if not email_otp.is_expired:
                # retrieving temporary token 
                temp_token=email_otp.temp_token
                
                return Response({"temp_token":str(temp_token),"message":"OTP verification successful.","success":True}, status=status.HTTP_200_OK)
            # if otp  not expired
            else:
                return Response({"message":"OTP has expired. Request for new one."}, status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response({"error":"Invalid OTP provided"}, status=status.HTTP_404_NOT_FOUND)