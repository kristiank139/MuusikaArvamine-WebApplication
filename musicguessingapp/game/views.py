from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Song, Playlist
import sqlite3
import random
from random import shuffle

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

def playlist_page(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    songs = list(playlist.songs.all())

    if 'song_order' not in request.session:
        request.session['song_order'] = list(range(len(songs)))
        shuffle(request.session['song_order'])

    song_order = request.session['song_order']
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': # Kui on AJAX request
        '''response = {'guessTitle': 'wrong', 'guessAuthor': 'wrong'}
        song_id = int(request.POST.get("song_id"))
        print(songs[song_id ].artist.lower())
        print(songs[song_id].title.lower())
        print(request.POST.get("guessTitle").lower())
        print(songs[song_id].title.lower())

        if request.POST.get("guessTitle").lower() == songs[song_id].title.lower(): # Kontrollib, kas laulu number ja arvamine sobitub andmebaasist võetud laulu numbri nimega
            print("õige")
            response.update({'guessTitle': 'correct'})
        if request.POST.get("guessAuthor").lower() == songs[song_id].artist.lower():
            response.update({'guessAuthor': 'correct'})

        return JsonResponse(response)'''
        print("here")
    
    if request.method == "POST": # Kontrollib, kas request method on post

        return redirect(f"/playlist/{playlist_id}/")
    
    if len(song_order) == 0:
        request.session['song_order'] = list(range(len(songs)))
        shuffle(request.session['song_order'])
        song_order = request.session['song_order']



    print(song_order)
    song_id = song_order.pop()
    print(song_id)
    page_obj = songs[song_id]

    # Valikvastuste saamine juhuslikult
    valikud = [songs[song_id].title]
    i = 0
    while i < 3:
        num = random.randint(0, len(songs) - 1)
        if songs[num].title not in valikud: # Vajalik, et ei tekiks mitut sama vastust
            valikud.append(songs[num].title)
            i += 1

    shuffle(valikud) # Suvaline järjekord
    print(valikud)
    
    context = {'playlist': playlist, 'songs': songs, 'page_obj': page_obj, 'playlist_id': playlist_id, 'song_id': song_id, 'valik1': valikud[0],
               "valik2": valikud[1], "valik3": valikud[2], "valik4": valikud[3], "id": valikud.index(songs[song_id].title)}
    return render(request, 'game/game.html', context)