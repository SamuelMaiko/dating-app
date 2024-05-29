from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('my-matches/', views.MyMatchesView.as_view(), name='my-matches'),    
]