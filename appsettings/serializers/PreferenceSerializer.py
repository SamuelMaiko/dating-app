from rest_framework import serializers
from appsettings.models import Preference

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ['min_age', 'max_age', 'location', 'gender', 'denomination']
