from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from userauth.models import CustomUser
from profiles.models import Favorite

class RemoveFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

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