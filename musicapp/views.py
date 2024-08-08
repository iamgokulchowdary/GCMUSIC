from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from functools import wraps
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from databaseapp.models import *
from .forms import *

# Create your views here.
def isuser(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.usertype == 'user':
                return view_func(request, *args, **kwargs)
            else:
                logout(request)
                return redirect('authapp:usersignin')
        else:
            return redirect('authapp:usersignin')
    return _wrapped_view

def HomePageView(request):
    topartists = Artist.objects.all().order_by('-followers').distinct()[:10]
    topplaylists = Playlist.objects.all().order_by('-followers').distinct()[:10]
    recentalbums = Album.objects.all().order_by('-datecreated').distinct()[:10]
    recentsongs = Song.objects.all().order_by('-dateuploaded').distinct()[:10]
    if request.user.is_authenticated:
        followingartists = Artist.objects.filter(followers = request.user.customuser).distinct()
        followingplaylists = Playlist.objects.filter(followers = request.user.customuser).distinct()
        yourplaylists = Playlist.objects.filter(owner = request.user.customuser).distinct()
    else:
        followingartists = None
        followingplaylists = None
        yourplaylists = None

    context = {'title':'HomePage', 'topartists':topartists, 'topplaylists':topplaylists, 'recentalbums':recentalbums, 'recentsongs':recentsongs, 'followingartists':followingartists, 'followingplaylists':followingplaylists, 'yourplaylists':yourplaylists}

    return render(request, 'musicapp/homepage.html', context=context)

@isuser
def EditProfilePageView(request):
    user = BaseUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
        return redirect('musicapp:editprofilepage')
    else:
        form = EditProfileForm(instance=user)
    countries = Country.objects.all()
    context = {'title':'Edit Profile', 'countries':countries}
    return render(request, 'musicapp/editprofilepage.html', context=context)

def ResultPageView(request):
    query = request.GET.get('q')

    if query:
        artists = Artist.objects.filter(
            Q(user__username__icontains=query)|
            Q(user__firstname__icontains=query)|
            Q(user__lastname__icontains=query)
            ).order_by('-followers').distinct()[:5]
        playlists = Playlist.objects.filter(name__icontains=query).order_by('-followers').distinct()[:5]
        songs = Song.objects.filter(name__icontains=query).distinct()[:5]
        albums = Album.objects.filter(name__icontains=query).distinct()[:5]
    else:
        artists = playlists = songs = albums = None
    
    context = {'title':'Results', 'artists':artists, 'playlists':playlists, 'songs':songs, 'albums':albums, 'query':query}

    return render(request, 'musicapp/resultpage.html', context=context)

def ArtistPageView(request, id):
    artist = get_object_or_404(Artist, id=id)
    songs = artist.songs.all().order_by('dateuploaded').distinct()[:10]
    albums = artist.albums.all().order_by('datecreated').distinct()[:10]
    context = {'title':'Artist', 'artist':artist, 'songs':songs, 'albums':albums}
    return render(request, 'musicapp/artistpage.html', context=context)

def AlbumPageView(request, id):
    album = get_object_or_404(Album, id=id)
    songs = album.songs.all().order_by('dateuploaded').distinct()[:10]
    context = {'title':'Album', 'songs':songs, 'album':album}
    return render(request, 'musicapp/albumpage.html', context=context)

def SongPageView(request, id):
    song = get_object_or_404(Song, id=id)
    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(owner=request.user.customuser).distinct()
    else:
        playlists = None
    context = {'title':'Song', 'song':song, 'playlists':playlists}
    return render(request, 'musicapp/songpage.html', context=context)

@isuser
def PlaylistsPageView(request):
    playlists = Playlist.objects.filter(owner=request.user.customuser).distinct()
    context = {'title':'Playlists', 'playlists':playlists}
    return render(request, 'musicapp/playlists.html', context=context)

def PlaylistPageView(request, id):
    playlist = Playlist.objects.get(id=id)
    context = {'title':'Playlist', 'playlist':playlist}
    return render(request, 'musicapp/playlistpage.html', context=context)

# Page Form or hidden page views
@isuser
def CreatePlaylistView(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.owner = request.user.customuser
            playlist.save()
            playlist.followers.add(request.user.customuser)
        return redirect('musicapp:playlistspage')
    else:
        form = PlaylistForm()
    return redirect('musicapp:playlistspage')

@isuser
def UpdatePlaylistView(request, id):
    playlist = get_object_or_404(Playlist, id=id)
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES, instance=playlist)
        if form.is_valid():
            form.save()
        return redirect('musicapp:playlistpage', id=id)
    else:
        form = PlaylistForm(instance=playlist)
    return redirect('musicapp:playlistpage', id=id)

@isuser
def AddToPlaylistView(request, id):
    if request.method == "POST":
        song = Song.objects.get(id=id)
        selected_playlists = request.POST.getlist('playlists')
        for playlistid in selected_playlists:
            playlist = Playlist.objects.get(id=playlistid)
            playlist.songs.add(song)
    return redirect('musicapp:songpage', id=id)

# Ajax Json Functions
@isuser
def FollowArtistJson(request, id):
    if request.method == 'POST':
        artist = Artist.objects.get(id=id)
        user = CustomUser.objects.get(user__id = request.user.id)

        if user in artist.followers.all():
            artist.followers.remove(user)
            action = 'unfollowed'
        else:
            artist.followers.add(user)
            action = 'followed'
        followerscount = artist.followers.count()
        return JsonResponse({'status': 'ok', 'followerscount':followerscount, 'action': action})
    return JsonResponse({'status': 'error'}, status=400)

@isuser
def FollowPlaylistJson(request, id):
    if request.method == 'POST':
        playlist = Playlist.objects.get(id=id)
        user = CustomUser.objects.get(user__id = request.user.id)

        if user in playlist.followers.all():
            playlist.followers.remove(user)
            action = 'unfollowed'
        else:
            playlist.followers.add(user)
            action = 'followed'
        followerscount = playlist.followers.count()
        return JsonResponse({'status': 'ok', 'followerscount':followerscount, 'action': action})
    return JsonResponse({'status': 'error'}, status=400)

@isuser
def DeleteSongFromPlaylistJson(request):
    if request.method == "POST":
        song_id = request.POST.get('songid')
        playlist_id = request.POST.get('playlistid')

        song = get_object_or_404(Song, id=song_id)
        playlist = get_object_or_404(Playlist, id=playlist_id)

        playlist.songs.remove(song)

        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'fail'}, status=400)