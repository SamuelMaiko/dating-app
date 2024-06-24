from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Our Dating App API",
      default_version='v1',
      description="This API powers our Dating App. It provides endpoints for user registration, authentication, preferences, and more.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="samuel.maiko.dev@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("chat/", include("chat.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
    path('api/', include('api.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   
   # replies to messages
   # timestamp correction
   # sending images
   # serializers
   # to representation
   
   # tomorrow
   # documenting chatapp apis

   #DISCOVER PAGE
   # display user username, image, age
   # 

   # searching and filtering
   # age
   # matching


   # TODO
   # shuffle discover and matches results
   # after message sent create or activate chat if not 
   # realtime updates
   # idle model (DeleteMessage)
   # serving images in production
   # handle environment variables
   