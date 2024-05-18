from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Logout the authenticated user.",
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
                description="User logged out successfully",
                examples={
                    "application/json": {
                        "message": "User logged out successfully"
                    }
                }
            ),
        },
        tags=['Authentication']
    )
    
    def post(self, request):
        request.user.auth_token.delete()
        response_dict=dict(message="User logged out successfully")
        return Response(response_dict, status=status.HTTP_200_OK)
