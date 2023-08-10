from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
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
    paginator = Paginator(Song.objects.all(),1) # Ainult 1 laul lehekülje kohta, vist on mõistlik muuta
    page_number = request.GET.get('page') # Siit saab laulu numbri, kui number on None, siis laul on esimene
    if page_number == None:
        page_number = 1
    
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj} # Annab HTML template'ile info, mis laul on
    return render(request, "game/game.html", context) # Näitab veebilehte, võtab template'i game templates/game folderist ja annab edasi context'o

def playlist_page(request, playlist_id, song_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    songs = playlist.songs.all()
    
    # Vaja võtta laulu id ja arvamine ning vaadata kas need on samad
    if request.method == "POST" and request.POST.get("guess"): # Kontrollib, kas request method on post ja guess on selle sees
        if request.POST.get("guess").lower() == songs[song_id - 1].title.lower(): # Kontrollib, kas laulu number ja arvamine sobitub andmebaasist võetud laulu numbri nimega
            print("õige")
            next_song = int(song_id) + 1
            total = total_songs(playlist_id)
            if next_song > total: #len(total_songs("db.sqlite3")): Kui rohkem lehti ei ole siis redirectib tagasi esimesele lehele
                return redirect(f"/playlist/{playlist_id}/1")
            else:
                return redirect(f"/playlist/{playlist_id}/{next_song}") # Kui õigesti ära arvad läheb järgmisele lehele, võibolla saaks ka nii teha, et kogu aeg oled samal lehel
        else:
            print("Vale")
            
    paginator = Paginator(songs, 1) # Üks laul lehekülje kohta
    page_obj = paginator.get_page(song_id)
    
    context = {'playlist': playlist, 'songs': songs, 'page_obj': page_obj}
    return render(request, 'game/game.html', context)