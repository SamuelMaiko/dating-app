from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from userauth.models import CustomUser
from profiles.models import HobbieProfile, Hobbie

class RemoveHobbieView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, hobbie_id):
        try:
            hobbie=Hobbie.objects.get(pk=hobbie_id)
        except Hobbie.DoesNotExist:
            return Response({'error':"Hobbie with id doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        profile=request.user.user_profile
        hobbieProfile=HobbieProfile.objects.filter(profile=profile, hobbie=hobbie)

        if not hobbieProfile.exists():
            return Response({'error':"Cannot remove a hobbie you don't have."}, status=status.HTTP_400_BAD_REQUEST) 
        
        hobbieProfile.delete()
        return Response({'message':f"{hobbie.title} removed successfully from hobbies."}, status=status.HTTP_204_NO_CONTENT)
        