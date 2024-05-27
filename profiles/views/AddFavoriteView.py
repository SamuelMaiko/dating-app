from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from userauth.models import CustomUser
from profiles.models import Favorite

class AddFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

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