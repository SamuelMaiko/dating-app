from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from userauth.models import CustomUser
from profiles.models import Favorite
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RemoveFavoriteView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Allows the logged user to remove a user from their favorites.",
    manual_parameters=[
        openapi.Parameter(
                'user_id',
                openapi.IN_PATH,
                description="Id of the user to unfavorite",
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
        204: openapi.Response(
            description="No content",
            examples={
                "application/json": {
                    "message": "User removed from favorites"
                }
                    }
    
            ),
            400: openapi.Response(
                description="Bad request",
                examples={
                    "application/json": {
                        "error": "User not in favorites"
                    }
                }
                ),
            403: openapi.Response(
                description="Forbidden",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action.",
                        "detail": "Authentication credentials were not provided."
                    }
                }
                ),
            404: openapi.Response(
                description="Not found",
                examples={
                    "application/json": {
                        "error": "User does not exist"
                    }
                }
                ),
        },
        tags=['Favorites']
    )


    def delete(self, request, user_id):
        try:
            user = request.user
            favorite_user = CustomUser.objects.get(pk=user_id)
            user_already_fav=Favorite.objects.filter(user=user, favorite=favorite_user).exists()
            if not user_already_fav:
                return Response({"error": "User not in favorites"}, status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.filter(user=user, favorite=favorite_user).delete()
            return Response({"message": "User removed from favorites"}, status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)