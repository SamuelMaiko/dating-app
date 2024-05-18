from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.Testing.as_view()),
    path('userauth/', include('userauth.urls')),
    path('profiles/', include('profiles.urls')),
    path('chatapp/', include('chatapp.urls')),
    path('matches/', include('matches.urls')),
    path('appsettings/', include('appsettings.urls')),
    path('groups/', include('groups.urls')),
    
]