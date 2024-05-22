from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('my-profile/', views.ProfileDetailView.as_view(), name='detail-profile'),
    path('user/<int:user_id>/', views.UserProfileView.as_view(), name='user-profile'),
    path('update/', views.ProfileUpdateAPIView.as_view(), name='update-profile'),
    path('temporary-update/', views.TemporaryProfileUpdateView.as_view(), name='update-profile'),
]