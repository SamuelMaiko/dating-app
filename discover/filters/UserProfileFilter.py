from django_filters import rest_framework as filters
from django.utils import timezone
from profiles.models import UserProfile

class UserProfileFilter(filters.FilterSet):
    min_age = filters.NumberFilter(field_name='date_of_birth', method='filter_min_age')
    max_age = filters.NumberFilter(field_name='date_of_birth', method='filter_max_age')
    gender = filters.CharFilter(field_name='gender')
    denomination = filters.CharFilter(field_name='denomination')
    location = filters.CharFilter(field_name='location')
    username = filters.CharFilter(field_name='user__username', lookup_expr='icontains')

    class Meta:
        model = UserProfile
        fields = ['gender', 'denomination', 'location', 'username']

    def filter_min_age(self, queryset, name, value):
        today = timezone.now().date()
        min_age = int(value)
        date_of_birth = today.replace(year=today.year - min_age)
        return queryset.filter(date_of_birth__lte=date_of_birth)

    def filter_max_age(self, queryset, name, value):
        today = timezone.now().date()
        max_age = int(value)
        date_of_birth = today.replace(year=today.year - max_age)
        return queryset.filter(date_of_birth__gte=date_of_birth)
