from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Change the authenticated user's password.",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Token token",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='Current password of the user'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New password for the user'),
            },
            required=['old_password', 'new_password']
        ),
        responses={
            200: openapi.Response(
                description="Password successfully updated.",
                examples={
                    "application/json": {
                        "message": "Password successfully updated."
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "detail": "New password must be different from old password."
                    },
                    "application/json": {
                        "detail": "Old password is incorrect."
                    },
                }
            ),
        },
        tags=['Profile']
    )

    def post(self, request):
        user = request.user
        data = request.data

        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        if old_password == new_password:
            return Response({'detail': 'New password must be different from old password.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        # Update the user's session to reflect the new password
        update_session_auth_hash(request, user)

        return Response({'message': 'Password successfully updated.'}, status=status.HTTP_200_OK)
