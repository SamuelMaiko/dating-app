from rest_framework import serializers
from appsettings.models import TemporaryPreference

class TemporaryPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryPreference
        fields = ['min_age', 'max_age', 'location', 'gender', 'denomination']
