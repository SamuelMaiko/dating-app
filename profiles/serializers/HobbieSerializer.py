from rest_framework import serializers
from profiles.models import Hobbie

class HobbieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Hobbie
        fields=['id', 'title']