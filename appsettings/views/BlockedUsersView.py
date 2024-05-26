from rest_framework.views import APIView
from appsettings.serializers import BlockedUserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from userauth.models import CustomUser
from chatapp.models import Block
from django.db.models import Subquery
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BlockedUsersView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request):
        blocked_users_ids=Block.objects.filter(blocker=request.user).values_list('blocked', flat=True)
        blocked_users=CustomUser.objects.filter(id__in=Subquery(blocked_users_ids))
        
        serializer=BlockedUserSerializer(blocked_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)