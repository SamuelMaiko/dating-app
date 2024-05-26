from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from chatapp.models import Block
from userauth.models import CustomUser
from django.http import Http404

class UnBlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_unblock = get_object_or_404(CustomUser, pk=user_id)
        except Http404:
            return Response({"error": "User with id not found"}, status=status.HTTP_404_NOT_FOUND)

        Block.objects.filter(blocker=request.user, blocked=user_to_unblock).delete()
        return Response({"message": "User unblocked successfully"}, status=status.HTTP_200_OK)
