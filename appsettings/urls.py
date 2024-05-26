from django.urls import path, include
from . import views

urlpatterns = [
    path('preferences/update/', views.PreferenceUpdateView.as_view(), name='update-preferences'),
    path('temporary-preferences/update/', views.TemporaryPreferenceUpdateView.as_view(), name='update-temporary-preferences'),
    path('blocked-users/', views.BlockedUsersView.as_view(), name='blocked-users'),
]