from django.urls import path
from . import views

urlpatterns = [
    path('profiles/', views.DiscoverView.as_view(), name='discover-profiles'),   
]