from django.urls import path
from .views import *

app_name = 'artistapp'
urlpatterns = [
    path('home/', HomePageView, name='homepage'),
    path('createalbum/', CreateAlbumView, name='createalbum'),
    path('uploadsong/', UploadSongView, name='uploadsong'),
    path('editprofile/', EditProfilePageView, name='editprofilepage'),
]