from django.urls import path
from .views import *

app_name = 'musicapp'
urlpatterns = [
    path('', HomePageView, name='homepage'),
    path('editprofile', EditProfilePageView, name='editprofilepage'),
    path('result', ResultPageView, name='resultpage'),
    path('playlists', PlaylistsPageView, name='playlistspage'),

    path('artist/<int:id>/', ArtistPageView, name='artistpage'),
    path('album/<int:id>/', AlbumPageView, name='albumpage'),
    path('song/<int:id>/', SongPageView, name='songpage'),
    path('playlist/<int:id>/', PlaylistPageView, name='playlistpage'),

    path('createplaylist', CreatePlaylistView, name='createplaylistview'),
    path('updateplaylist/<int:id>/', UpdatePlaylistView, name='updateplaylistview'),
    path('addtoplaylist/<int:id>', AddToPlaylistView, name='addtoplaylistview'),

    path('artist/<int:id>/follow/', FollowArtistJson, name='follow_artist'),
    path('playlist/<int:id>/follow/', FollowPlaylistJson, name='follow_playlist'),
    path('deletesongfromplaylist/', DeleteSongFromPlaylistJson, name='delete_song_from_playlist'),
]