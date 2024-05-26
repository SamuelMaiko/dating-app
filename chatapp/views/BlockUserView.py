from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from chatapp.models import Block
from userauth.models import CustomUser
from django.shortcuts import get_object_or_404
from django.http import Http404

class BlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_block = get_object_or_404(CustomUser, pk=user_id)
        except Http404:
            return Response({"error": "User with id not found"}, status=status.HTTP_404_NOT_FOUND)

        Block.objects.get_or_create(blocker=request.user, blocked=user_to_block)
        return Response({"message": "User blocked successfully"}, status=status.HTTP_201_CREATED)
