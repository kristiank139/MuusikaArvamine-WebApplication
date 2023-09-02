from django.contrib import admin
from .models import Song, Playlist

# Register your models here.
#admin.site.register(Song)

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    pass

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    pass