from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import UserPhotoSerializer

class AddPhotosView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        serializer = UserPhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    