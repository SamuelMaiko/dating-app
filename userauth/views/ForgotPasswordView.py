from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from userauth.models import CustomUser
from rest_framework import status
from rest_framework.views import APIView
from userauth.signals import send_otp_signal
from userauth.HelperFunctions import generate_otp
from userauth.models import EmailOTP
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(   
        operation_description="Request a password reset by providing the user's email.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the user'),
            },
            required=['email']
        ),
        responses={
            200: openapi.Response(
                description="OTP sent to email",
                examples={
                    "application/json": {
                        "message": "OTP sent to email"
                    }
                }
            ),
            404: openapi.Response(
                description="User Not Found",
                examples={
                    "application/json": {
                        "message": "User with email does not exist."
                    }
                }
            ),
        },
        tags=['Forgot Password']
    )

    def post(self, request):
        email=request.data.get("email")
        try:
            user=CustomUser.objects.filter(email=email).first()
        except CustomUser.DoesNotExist:
            return Response({'message':"User with email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # generating new otp (because we use the same for email verification earlier)
        new_otp=generate_otp()
        # updating the otp
        EmailOTP.objects.filter(user=user).update(otp=new_otp)
        # signal to send otp to user's email
        send_otp_signal.send(sender=None, user=user)
        
        return Response({'message':"OTP sent to email"}, status=status.HTTP_200_OK)
        
        