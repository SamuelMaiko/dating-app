from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('my-profile/', views.ProfileDetailView.as_view(), name='detail-profile'),
    path('user/<int:user_id>/', views.UserProfileView.as_view(), name='user-profile'),
    path('update/', views.ProfileUpdateAPIView.as_view(), name='update-profile'),
    path('temporary-update/', views.TemporaryProfileUpdateView.as_view(), name='update-profile'),
    path('my-photos/', views.MyPhotosView.as_view(), name='my-photos'),
    path('photos/user/<int:user_id>/', views.UserPhotosView.as_view(), name='user-photos'),
    path('my-photos/add/', views.AddPhotosView.as_view(), name='add-photos'),
    path('my-photos/delete/<int:photo_id>/', views.DeletePhotosView.as_view(), name='delete-photo'),
    path('my-favorites/', views.MyFavoriteView.as_view(), name='my-favorites'),
    path('favorites/add/<int:user_id>/', views.AddFavoriteView.as_view(), name='add-favorite'),
    path('favorites/remove/<int:user_id>/', views.RemoveFavoriteView.as_view(), name='remove-favorite'),
    path('hobbies/', views.HobbiesView.as_view(), name='hobbies'),
    path('my-hobbies/', views.MyHobbiesView.as_view(), name='my-hobbies'),
    path('hobbies/user/<int:user_id>/', views.UserHobbiesView.as_view(), name='user-hobbies'),
    path('my-hobbies/add/<int:hobbie_id>/', views.AddHobbieView.as_view(), name='add-hobbie'),
    path('my-hobbies/remove/<int:hobbie_id>/', views.RemoveHobbieView.as_view(), name='remove-hobbie'),
]