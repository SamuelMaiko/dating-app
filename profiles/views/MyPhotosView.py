from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import UserPhotoSerializer

class MyPhotosView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request):
        user=request.user
        
        photos=user.photos.all()
        serializer=UserPhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    