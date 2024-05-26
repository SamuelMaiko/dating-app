from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import UserPhotoSerializer
from userauth.models import CustomUser

class UserPhotosView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request, user_id):
        try:
            user=CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error":"User with id doesn't exist."}, status=status.HTTP_404_NOT_FOUND)
        
        photos=user.photos.all()
        serializer=UserPhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    