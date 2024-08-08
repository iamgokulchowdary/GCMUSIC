from django import forms
from databaseapp.models import *

class CreateAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'image']

class UploadSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['name', 'album', 'composer', 'artists', 'language', 'genre', 'lyrics', 'file']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = BaseUser
        fields = ['firstname', 'lastname', 'phoneno', 'address', 'country', 'image']