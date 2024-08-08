from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from databaseapp.models import CustomUser, Artist
from .forms import *

# Create your views here.
def UserSignUpView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.usertype = 'user'
            user.save()
            CustomUser.objects.create(user=user)
            login(request, user)

            return redirect('musicapp:homepage')
    else:
        form = SignUpForm()
    
    context = {'title':'Sign Up', 'form':form, 'authapp':'authapp', 'authtype':'User'}
    return render(request, 'authapp/signup.html', context=context)

def UserSignInView(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username = username, password = password)
            if user is not None:
                if user.usertype == 'user':
                    login(request, user)
                    return redirect('musicapp:homepage')
                else:
                    form.add_error(None, 'Invalid Username and Password')
            else:
                form.add_error(None, 'Invalid Username and Password')
    else:
        form = SignInForm()

    context = {'title' : 'Sign In', 'form' : form, 'authapp':'authapp', 'authtype':'User'}
    return render(request, 'authapp/signin.html', context = context)

def ArtistSignUpView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.usertype = 'artist'
            user.save()
            Artist.objects.create(user=user)
            login(request, user)

            return redirect('artistapp:homepage')
    else:
        form = SignUpForm()
    
    context = {'title':'Artist SignUp', 'form':form, 'authapp':'authapp', 'authtype':'Artist'}
    return render(request, 'authapp/signup.html', context=context)

def ArtistSignInView(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username = username, password = password)
            if user is not None:
                if user.usertype == 'artist':
                    login(request, user)
                    return redirect('artistapp:homepage')
                else:
                    form.add_error(None, 'Invalid Username and Password')
            else:
                form.add_error(None, 'Invalid Username and Password')
    else:
        form = SignInForm()

    context = {'title' : 'signin', 'form' : form, 'authapp':'authapp', 'authtype':'Artist'}
    return render(request, 'authapp/signin.html', context = context)

def UserChangePasswordView(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('musicapp:editprofilepage')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form}
    return render(request, 'authapp/changepassword.html', context=context)

def ArtistChangePasswordView(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('artistapp:editprofilepage')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form}
    return render(request, 'authapp/changepassword.html', context=context)

def LogOutView(request):
    logout(request)
    return redirect('musicapp:homepage')