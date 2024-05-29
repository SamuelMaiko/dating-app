from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.models import Favorite
from profiles.serializers import FavoriteSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class MyFavoriteView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
    operation_description="Retrieves all the favorites of the logged user.",
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
            description="Success",
            examples={
                "application/json": [
                                {
                                    "user_id": 6,
                                    "username": "sam",
                                    "profile_picture": "/media/profile-pictures/default.jpg",
                                    "date_of_birth": "2020-10-10"
                                },
                                {
                                    "user_id": 3,
                                    "username": "enock",
                                    "profile_picture": "/media/profile-pictures/wallpaperflare.com_wallpaper_1_fE0Jszv.jpg",
                                    "date_of_birth": "2017-05-09"
                                }
                            ]
                    }
    
            ),
        },
        tags=['Favorites']
    )

    def get(self, request):
        try:
            user = request.user
            favorites = Favorite.objects.filter(user=user)
            serializer = FavoriteSerializer(favorites, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
