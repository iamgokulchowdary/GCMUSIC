from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from databaseapp.models import BaseUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = BaseUser
        fields = ['username', 'email', 'password1', 'password2']

class SignInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)