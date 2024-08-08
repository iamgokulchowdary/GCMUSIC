from django import forms
from databaseapp.models import *

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'image']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = BaseUser
        fields = ['firstname', 'lastname', 'phoneno', 'address', 'country', 'image']