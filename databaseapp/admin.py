from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

# Register your models here.
class CustomBaseUser(UserAdmin):
    model = BaseUser
    list_display = ('username', 'email', 'phoneno', 'usertype', 'country')
    fieldsets = (
        (None, {'fields' : ('username', 'password')}),
        ('Personal Details', {'fields' : ('firstname', 'lastname', 'email', 'phoneno', 'address', 'country', 'image')})
    )

admin.site.register(BaseUser, CustomBaseUser)
admin.site.register(CustomUser)
admin.site.register(Artist)
admin.site.register(Playlist)
admin.site.register(Song)
admin.site.register(Album)

admin.site.register(Language)
admin.site.register(Genre)
admin.site.register(Country)