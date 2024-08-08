from django.urls import path
from .views import *

app_name = 'authapp'
urlpatterns = [
    path('usersignin', UserSignInView, name='usersignin'),
    path('usersignup', UserSignUpView, name='usersignup'),
    path('artistsignin', ArtistSignInView, name='artistsignin'),
    path('artistsignup', ArtistSignUpView, name='artistsignup'),
    path('user/changepassword', UserChangePasswordView, name='userchangepassword'),
    path('artist/changepassword', ArtistChangePasswordView, name='artistchangepassword'),
    path('logout', LogOutView, name='logout')
]