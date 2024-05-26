from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import HobbieSerializer
from profiles.models import Hobbie, HobbieProfile

class AddHobbieView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request, hobbie_id):
        try:
            hobbie=Hobbie.objects.get(pk=hobbie_id)
        except Hobbie.DoesNotExist:
            return Response({'error':"Hobbie with id doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        user_profile=request.user.user_profile
        hobbieprofile=HobbieProfile.objects.filter(profile=user_profile, hobbie=hobbie)

        if hobbieprofile.exists():
            return Response({'error':"Cannot add already added hobbie."}, status=status.HTTP_400_BAD_REQUEST)    
        
        HobbieProfile.objects.create(profile=user_profile, hobbie=hobbie)
        return Response({'message':f"{hobbie.title} added successfully to hobbies."}, status=status.HTTP_200_OK)