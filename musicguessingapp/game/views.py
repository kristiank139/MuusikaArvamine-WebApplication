from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Song
from django.http import  HttpResponseRedirect
import sqlite3
from pytube import YouTube, Playlist
import os

# Create your views here.

def index(request):
    paginator = Paginator(Song.objects.all(),1)
    page_number = request.GET.get('page', 1) # Siit saab laulu numbri, kui number on None, siis laul on esimene
    page_obj = paginator.get_page(page_number)

    if page_number == None:
        page_number = 1
    if request.method == "POST" and request.POST.get("guess"): # Kontrollib, kas request method on post
        if request.POST.get("guess").lower() == song_names("db.sqlite3", page_number).lower(): # Kontrollib, kas laulu number ja arvamine sobitub andmebaasist võetud laulu numbri nimega
            print("õige")
            next_page = int(page_number) + 1
            if next_page > len(total_songs("db.sqlite3")): # Kui rohkem lehti ei ole siis redirectib tagasi esimesele lehele
                return redirect(f"/?page=1")
            else:
                return redirect(f"/?page={next_page}") # Kui õigesti ära arvad läheb järgmisele lehele, võibolla saaks ka nii teha, et kogu aeg oled samal lehel
            
    link = request.POST.get("link") # Siit tuleb link
    exists = song_exists(link)
    
    if exists:
            duplicate = "Laul on juba olemas"
    else:
        duplicate = None
        download_song(link)

    context={"page_obj":page_obj, "duplicate":duplicate}
    return render(request, "game/game.html", context)

def song_exists(link):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT EXISTS(SELECT 1 FROM game_song WHERE audio_link=?)", (link,))
    exists = c.fetchone()[0]
    conn.close()
    return exists

def download_song(link):
    if link:
        if "playlist" in link:
            download_playlist(link)
        else:
            download_single_song(link)

def download_playlist(link):
    p = Playlist(link)
    for video in p.videos:
        if not song_exists(video.watch_url):
            print("why")
            filename = video.streams.first().title.replace(" ", "") + ".mp3"
            duration = durationify(video.length)
            video.streams.first().download(f"{os.getcwd()}/media", filename=filename)
            writesongs("db.sqlite3", video.watch_url, filename, duration, link)

def download_single_song(link):
    if not song_exists(link):
        yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
        ys = yt.streams.filter(file_extension='mp4').first()
        filename = ys.title.replace(" ", "") + ".mp3"
        duration = durationify(yt.length)
        ys.download(f"{os.getcwd()}/media", filename=filename)
        writesongs("db.sqlite3", link, filename, duration, None)

def song_names(db, song_num):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT * FROM 'game_song'")
    return c.fetchall()[int(song_num) - 1][1]

def total_songs(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT * FROM 'game_song'")
    return c.fetchall()

def durationify(duration): # Teeb sekundid õigeks formaadiks
    seconds = duration % 60
    minutes = int((duration - seconds) / 60)
    return f"{str(minutes)}:{str(seconds)}"

def writesongs(db, link, filename, duration, pLink): # Kirjutab andmed database'i
    conn = sqlite3.connect(db)
    c = conn.cursor()
    
    try:
        # Create a new record
        c.execute("SELECT MAX(id) FROM game_song")
        result = c.fetchone()[0] or 0
        next_id = result + 1
        sql = "INSERT INTO game_song (id, title, artist, image, audio_file, audio_link, duration, playlist_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        c.execute(sql, (next_id, 'b', 'c', "GermanShephard.jpg", filename, link, duration, pLink))
    
        # Commit changes
        conn.commit()

    finally:
        conn.close()