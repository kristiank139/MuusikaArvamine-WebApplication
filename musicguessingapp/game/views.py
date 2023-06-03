from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Song
from django.http import  HttpResponseRedirect
import sqlite3
from pytube import YouTube
import os

# Create your views here.

def index(request):
    paginator = Paginator(Song.objects.all(),1)
    page_number = request.GET.get('page') # Siit saab laulu numbri, kui number on None, siis laul on esimene
    if page_number == None:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    if request.method == "POST" and request.POST.get("guess"): # Kontrollib, kas request method on post
        if request.POST.get("guess").lower() == song_names("db.sqlite3", page_number).lower(): # Kontrollib, kas laulu number ja arvamine sobitub andmebaasist võetud laulu numbri nimega
            print("correct")
            next_page = int(page_number) + 1
            if next_page > len(total_songs("db.sqlite3")):
                return redirect(f"/?page=1")
            else:
                return redirect(f"/?page={str(next_page)}")
    link = request.POST.get("playlist")
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    try:
        # Create a new record
        linkSelect = "SELECT audio_link FROM game_song"
        c.execute(linkSelect)
        for list in c.fetchall():
            if link in list:
                exists = True
            else:
                exists = False
        if exists:
            duplicate = "Laul on juba olemas"
        else:
            conn.close()
            duplicate = None
            Download(request, link)
    finally:
        conn.close()
    context={"page_obj":page_obj, "duplicate":duplicate}
    return render(request, "game/game.html", context)

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

def durationify(duration):
    seconds = duration % 60
    minutes = int((duration - seconds) / 60)
    return f"{str(minutes)}:{str(seconds)}"

def Download(request, link):
    if link:
        yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
        ys = yt.streams.filter(file_extension='mp4').first()
        filename = ys.title.replace(" ", "") + ".mp3"
        duration = durationify(yt.length)
        ys.download(f"{os.getcwd()}/media", filename=filename) # Media folderisse lähevad kõik laulufailid
        writesongs("db.sqlite3", link, filename, duration)

def writesongs(db, link, filename, duration):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    try:
        # Create a new record
        nextId = "SELECT id FROM game_song"
        c.execute(nextId)
        all = c.fetchall()
        if len(all) == 0:
            result = 1
        elif len(all) == 1:
            result = 2
        else:
            result = int(all[-1][0]) + 1
        sql = "INSERT INTO game_song (id, title, artist, image, audio_file, audio_link, duration) VALUES (?, ?, ?, ?, ?, ?, ?)"
        c.execute(sql, (result, 'b', 'c', "GermanShephard.jpg", filename, link, duration))
    
        # Commit changes
        conn.commit()
    
        print("Record inserted successfully")
    finally:
        conn.close()