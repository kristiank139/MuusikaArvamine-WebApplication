from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Song, Playlist
import sqlite3

# Create your views here.

def total_songs(playlistid): # Annab numbri, kui palju laule on playlist'is
    # Ühendamine andmebaasiga
    conn = sqlite3.connect("db.sqlite3")

    # Leiab kõik laulude arv, mille playlist_id on playlistid
    query = f"SELECT COUNT(*) FROM game_playlist_songs WHERE playlist_id = ?;"
    cursor = conn.execute(query, (playlistid,))
    count = cursor.fetchone()[0]

    conn.close()

    return count

def index(request):
    conn = sqlite3.connect("db.sqlite3")

    # Leiab kõik laulude arv, mille playlist_id on playlistid
    query = f"SELECT title FROM game_playlist"
    cursor = conn.execute(query)
    count = cursor.fetchall()
    playlistid = []
    for playlist in count:
        playlistid.append(playlist[0])

    conn.close()
    return render(request, "game/avaleht.html", {"playlistid": playlistid}) # Näitab veebilehte, võtab template'i game templates/game folderist ja annab edasi context'o

def playlist_page(request, playlist_id, song_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    songs = playlist.songs.all()
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': # Kui on AJAX request
        if request.POST.get("guess").lower() == songs[song_id - 1].title.lower(): # Kontrollib, kas laulu number ja arvamine sobitub andmebaasist võetud laulu numbri nimega
            print("õige")
            return JsonResponse({'guess': 'correct'})
        else:
            return JsonResponse({'guess': 'wrong'})
    
    # Vaja võtta laulu id ja arvamine ning vaadata kas need on samad
    if request.method == "POST": # Kontrollib, kas request method on post ja guess on selle sees

        next_song = int(song_id) + 1
        total = total_songs(playlist_id)
        if next_song > total: #len(total_songs("db.sqlite3")): Kui rohkem lehti ei ole siis redirectib tagasi esimesele lehele
            return redirect(f"/playlist/{playlist_id}/1")
        else:
            return redirect(f"/playlist/{playlist_id}/{next_song}") # Kui õigesti ära arvad läheb järgmisele lehele, võibolla saaks ka nii teha, et kogu aeg oled samal lehel

    paginator = Paginator(songs, 1) # Üks laul lehekülje kohta
    page_obj = paginator.get_page(song_id)
    
    context = {'playlist': playlist, 'songs': songs, 'page_obj': page_obj, 'playlist_id': playlist_id, 'song_id': song_id}

    return render(request, 'game/game.html', context)

