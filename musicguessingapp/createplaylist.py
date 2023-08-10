
'''# Siin ma saan luua playliste, tegin selleks eraldi faili, seda peab vastavalt muutma iga kord kui tahad teha playlisti

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicguessingapp.settings')

django.setup()

playlist1 = Playlist.objects.create(title='Playlist 1')

# Paneb laulu, millel on kindel id võrduma muutujaga
song1 = Song.objects.get(id=1)
song2 = Song.objects.get(id=2)

# Lisab laulud playlisti
if song1 not in playlist1.songs.all():
    playlist1.songs.add(song1)

if song2 not in playlist1.songs.all():
    playlist1.songs.add(song2)

playlist2 = Playlist.objects.create(title='Playlist 2')

song3 = Song.objects.get(id=3)
playlist2.songs.add(song3)'''

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicguessingapp.settings')

django.setup()

from game.models import Song, Playlist

playlist = Playlist.objects.create(title='Keskaja playlist')

laul1 = Song.objects.get(id=4)
laul2 = Song.objects.get(id=5)
#laul3 = Song.objects.get(id=3)
#laul4 = Song.objects.get(id=4)

playlist.songs.add(laul1)
playlist.songs.add(laul2)
#playlist.songs.add(laul3)
#playlist.songs.add(laul4)