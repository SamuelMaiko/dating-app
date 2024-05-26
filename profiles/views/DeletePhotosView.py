from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import UserPhotoSerializer
from profiles.permissions import IsPhotoOwner
from profiles.models import UserPhoto

class DeletePhotosView(APIView):
    permission_classes=[IsAuthenticated, IsPhotoOwner]
    
    def delete(self, request, photo_id):
        try:
            photo=UserPhoto.objects.get(pk=photo_id)
        except UserPhoto.DoesNotExist:
            return Response({"error":"Photo with provided id does not exist"},  status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, photo)

        photo.delete()
        return Response({"message":"Photo deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    