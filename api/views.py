from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from chatapp.HelperFunctions import send_message_to_group
from userauth.models import CustomUser
from .signals import cust

# Create your views here.
class Testing(APIView):
    def post(self, request):
        
        user= CustomUser.objects.get(id=6)
        
        user.username="sami"
        user.save()
        
        # send_message_to_group("chat", "Thcjhgduhckjhc")
        cust.send(sender=None,gname="chat", message="Thcjhgduhckjhc")
        
        return HttpResponse("Hello there")
        