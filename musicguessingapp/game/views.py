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
    page_number = request.GET.get('page') # Siit saab laulu numbri, kui number on None, siis laul on esimene
    if page_number == None:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    if request.method == "POST" and request.POST.get("guess"): # Kontrollib, kas request method on post
        if request.POST.get("guess").lower() == song_names("db.sqlite3", page_number).lower(): # Kontrollib, kas laulu number ja arvamine sobitub andmebaasist võetud laulu numbri nimega
            print("õige")
            next_page = int(page_number) + 1
            if next_page > len(total_songs("db.sqlite3")): # Kui rohkem lehti ei ole siis redirectib tagasi esimesele lehele
                return redirect(f"/?page=1")
            else:
                return redirect(f"/?page={str(next_page)}") # Kui õigesti ära arvad läheb järgmisele lehele, võibolla saaks ka nii teha, et kogu aeg oled samal lehel
            
    link = request.POST.get("link") # Siit tuleb link
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    exists = False

    try:
        linkSelect = "SELECT audio_link FROM game_song" # Valib kõik lingid
        c.execute(linkSelect)
        links = c.fetchall() # Tekib list, kus on tuple'id, kus on lingid (link, )
        if "playlist" in link: # Playlistide jaoks, kontrollib, et samasuguseid laule ei oleks. Võibolla teha pigem selline süsteem, kus database'is on playlisti link ka, ja alla laadida need, mida veel ei ole.
            p = Playlist(link)
            urls = p.video_urls
            for list in links:
                for url in urls:
                    if url in list:
                        exists = True
                        break
        else:
            for list in links:
                if link in list:
                    exists = True
                    break
                else:
                    exists = False
        if exists:
            duplicate = "Laul on juba olemas"
        else:
            conn.close()
            duplicate = None
            Download(link)
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

def durationify(duration): # Teeb sekundid õigeks formaadiks
    seconds = duration % 60
    minutes = int((duration - seconds) / 60)
    return f"{str(minutes)}:{str(seconds)}"

def Download(link): # Laeb alla laulu(d) media folderisse
    if link:
        if "playlist" in link:
            p = Playlist(link)
            i = 0
            for video in p.videos:
                filename = video.streams.first().title.replace(" ", "") + ".mp3"
                duration = durationify(video.length)
                video.streams.first().download(f"{os.getcwd()}/media", filename=filename)
                writesongs("db.sqlite3", p.video_urls[i], filename, duration)
                i += 1

        else:
            yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
            ys = yt.streams.filter(file_extension='mp4').first()
            filename = ys.title.replace(" ", "") + ".mp3"
            duration = durationify(yt.length)
            ys.download(f"{os.getcwd()}/media", filename=filename) # Media folderisse lähevad kõik laulufailid
            writesongs("db.sqlite3", link, filename, duration)

def writesongs(db, link, filename, duration): # Kirjutab andmed database'i
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