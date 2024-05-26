from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import HobbieSerializer
from userauth.models import CustomUser
from profiles.models import Hobbie, HobbieProfile, UserProfile
from django.db.models import Subquery

class UserHobbiesView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request, user_id):
        try:
            user=CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error":"User with id doesn't exist."}, status=status.HTTP_404_NOT_FOUND)
        
        profile=UserProfile.objects.get(user=user)
        hobbies_ids=HobbieProfile.objects.filter(profile=profile).values_list("hobbie", flat=True)
        hobbies=Hobbie.objects.filter(id__in=Subquery(hobbies_ids))
        serializer=HobbieSerializer(hobbies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    