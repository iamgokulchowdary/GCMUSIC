from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import *
from databaseapp.models import *
from functools import wraps
    
def isartist(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.usertype == 'artist':
                return view_func(request, *args, **kwargs)
            else:
                logout(request)
                return redirect('authapp:artistsignin')
        else:
            return redirect('authapp:artistsignin')
    return _wrapped_view

@isartist
def HomePageView(request):
    context = {'title':'Artist HomePage'}
    return render(request, 'artistapp/homepage.html', context=context)

@isartist
def CreateAlbumView(request):
    if request.method == 'POST':
        form = CreateAlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)
            artist = Artist.objects.get(user = request.user)
            album.owner = artist
            album.save()
            artist.albums.add(album)
            return redirect('artistapp:homepage')
    else:
        form = CreateAlbumForm()
    context = {'title':'Add Album', 'form': form}
    return render(request, 'artistapp/createalbum.html', context)

@isartist
def UploadSongView(request):
    if request.method == 'POST':
        form = UploadSongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save()

            albumname = form.cleaned_data.get('album')
            album = Album.objects.get(id = albumname.id)
            album.songs.add(song)

            artistnames = form.cleaned_data.get('artists')
            for artistname in artistnames:
                artist = Artist.objects.get(id = artistname.id)
                artist.songs.add(song)
            
            languagename = form.cleaned_data.get('language')
            language = Language.objects.get(id = languagename.id)
            language.songs.add(song)

            genrenames = form.cleaned_data.get('genre')
            for genrename in genrenames:
                genre = Genre.objects.get(id = genrename.id)
                genre.songs.add(song)

            lyricsname = form.cleaned_data.get('lyrics')
            lyrics = Artist.objects.get(id = lyricsname.id)
            lyrics.songs.add(song)

            composername = form.cleaned_data.get('composer')
            composer = Artist.objects.get(id = composername.id)
            composer.songs.add(song)

            return redirect('artistapp:homepage')
    else:
        form = UploadSongForm()
    artists = Artist.objects.all()
    albums = Album.objects.all()
    languages = Language.objects.all()
    genres = Genre.objects.all()
    context = {'title':'Upload Song', 'form': form, 'albums':albums, 'artists':artists, 'languages':languages, 'genres':genres}
    return render(request, 'artistapp/uploadsong.html', context)
    
@isartist
def EditProfilePageView(request):
    user = BaseUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        return redirect('artistapp:editprofilepage')
    else:
        form = EditProfileForm(instance=user)
    countries = Country.objects.all()
    context = {'title':'Edit Profile', 'countries':countries}
    return render(request, 'artistapp/editprofilepage.html', context=context)