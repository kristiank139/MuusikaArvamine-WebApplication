from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Song
from django.http import  HttpResponseRedirect
import sqlite3

# Create your views here.

def index(request):
    paginator = Paginator(Song.objects.all(),1)
    page_number = request.GET.get('page') # Siit saab laulu numbri, kui number on None, siis laul on esimene
    if page_number == None:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    context={"page_obj":page_obj}
    if request.method == "POST": # Kontrollib, kas request method on post
        if request.POST.get("guess").lower() == song_names(db="db.sqlite3", song_num=page_number).lower(): # Kontrollib, kas laulu number ja arvamine sobitub andmebaasist võetud laulu numbri nimega
            print("correct")
            next_page = int(page_number) + 1
            if next_page > len(total_songs("db.sqlite3")):
                return redirect(f"/?page=1")
            else:
                return redirect(f"/?page={str(next_page)}")
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