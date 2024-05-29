from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from userauth.models import CustomUser
from profiles.models import Favorite
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class AddFavoriteView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Allows the logged user to favorite another user.",
    manual_parameters=[
        openapi.Parameter(
                'user_id',
                openapi.IN_PATH,
                description="Id of the user to be favorited.",
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
        200: openapi.Response(
            description="Success",
            examples={
                "application/json": {
                    "status": "User added to favorites"
                }
                    }
    
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "error": "You cannot favorite yourself",
                        "error": "User already favorited"
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
                ),
            404: openapi.Response(
                description="Not Found",
                examples={
                    "application/json": {
                        "error": "User does not exist"
                    }
                }
                )
        },
        tags=['Favorites']
    )


    def post(self, request, user_id):
        try:
            user = request.user
            favorite_user = CustomUser.objects.get(pk=user_id)
            if user != favorite_user:
                user_already_fav=Favorite.objects.filter(user=user, favorite=favorite_user).exists()
                if user_already_fav:
                    return Response({"error": "User already favorited"}, status=status.HTTP_400_BAD_REQUEST)
                
                Favorite.objects.create(user=user, favorite=favorite_user)
                return Response({"status": "User added to favorites"}, status=status.HTTP_200_OK)
            return Response({"error": "You cannot favorite yourself"}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)