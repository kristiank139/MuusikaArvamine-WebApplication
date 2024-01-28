from django.urls import path, include

from . import views

app_name = "App"

## Ajutiselt on praegu vaja playlist'is olevate laulude mängimiseks minna http://127.0.0.1:8000/playlist/(playlisti number)/(laulu number playlistis, esimene laul on 1)
#urlpatterns = [
#   path("", views.index, name="index"),
#   path("playlist/<int:playlist_id>/<int:song_id>", views.playlist_page, name="playlist"),
#]


urlpatterns = [
    path("", views.index, name="index"),
    path("playlist/<int:playlist_id>/", views.playlist_page, name="playlist"),

]
