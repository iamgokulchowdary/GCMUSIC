from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

usertypes = [('user', 'user'), ('artist', 'artist')]

class BaseUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True, blank=False)
    email = models.EmailField(blank=False, unique=True)
    firstname = models.CharField(max_length=120, blank=True, null=True)
    lastname = models.CharField(max_length=120, blank=True, null=True)
    phoneno = models.BigIntegerField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    country = models.ForeignKey('Country', on_delete=models.PROTECT, null=True,  related_name='baseusercountry')
    image = models.ImageField(upload_to='profileimages', blank=True, null=True)
    usertype = models.CharField(max_length=15, blank=False, choices=usertypes)
    datejoined = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Base User'
    
    def __str__(self):
        return self.username

class CustomUser(models.Model):
    user = models.OneToOneField('BaseUser', on_delete=models.CASCADE)
    playlists = models.ManyToManyField('Playlist', related_name='userplaylists')
    languages = models.ManyToManyField('Language', related_name='userlanguages')

    def __str__(self):
        return str(self.user)

class Artist(models.Model):
    user = models.OneToOneField('BaseUser', on_delete=models.CASCADE)
    bio = models.TextField(blank=False)
    songs = models.ManyToManyField('Song', related_name='artistsongs')
    albums = models.ManyToManyField('Album', related_name='artistalbums')
    followers = models.ManyToManyField('CustomUser', related_name='artistfollowers')

    def __str__(self):
        return str(self.user)
    
class Song(models.Model):
    name = models.CharField(max_length=120, blank=False)
    album = models.ForeignKey('Album', on_delete=models.CASCADE, related_name='songalbum')
    artists = models.ManyToManyField('Artist', related_name='songartists')
    language = models.ForeignKey('Language', on_delete=models.PROTECT, related_name='songlanguage')
    genre = models.ManyToManyField('Genre', related_name='songgenre')
    composer = models.ForeignKey('Artist', on_delete=models.PROTECT, related_name='songcomposer')
    lyrics = models.ForeignKey('Artist', on_delete=models.PROTECT, related_name='songlyrics')
    file = models.FileField(upload_to='songfiles', blank=False)
    dateuploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    name = models.CharField(max_length=120, blank=False)
    owner = models.ForeignKey('Artist', on_delete=models.PROTECT, related_name='albumowner')
    songs = models.ManyToManyField('Song', related_name='albumsongs', blank=True)
    image = models.ImageField(upload_to='albumcover', blank=False)
    datecreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Playlist(models.Model):
    name = models.CharField(max_length=120, blank=False)
    owner = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='playlistowner')
    songs = models.ManyToManyField('Song', related_name='playlistsongs', blank=True)
    image = models.ImageField(upload_to='playlistcover', blank=False)
    followers = models.ManyToManyField('CustomUser', related_name='playlistfollowers', blank=True)
    datecreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=120, blank=False)
    songs = models.ManyToManyField('Song', related_name='languagesongs')

    def __str__(self):
        return self.language

class Genre(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=120, blank=False)
    songs = models.ManyToManyField('Song', related_name='genresongs')

    def __str__(self):
        return self.genre

class Country(models.Model):
    name = models.CharField(max_length=120, blank=True)
    users = models.ManyToManyField('CustomUser', related_name='countryusers')

    def __str__(self):
        return self.country