from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.ProfileDetailView.as_view(), name='detail-profile'),
    path('update/', views.ProfileUpdateAPIView.as_view(), name='update-profile'),
    path('temporary-update/', views.TemporaryProfileUpdateView.as_view(), name='update-profile'),
]