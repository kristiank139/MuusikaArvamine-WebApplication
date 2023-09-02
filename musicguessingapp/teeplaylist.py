# Siin ma saan luua playliste, tegin selleks eraldi faili, seda peab vastavalt muutma iga kord kui tahad teha playlisti

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicguessingapp.settings')

django.setup()

from game.models import Song, Playlist

# Teeb playlist'i kuhu saan lisada laule, võib teha korraga ka mitu
playlist = Playlist.objects.create(title='Keskaja playlist')

# Siin võtan laulud andmebaasist nende id kaudu, id tuleb laulude lisamise järjekorras, esimese lisatud laulu id on 1 jne
laul1 = Song.objects.get(id=4)
laul2 = Song.objects.get(id=5)
#laul3 = Song.objects.get(id=3)
#laul4 = Song.objects.get(id=4)

# Lisan laulud playlist'i
playlist.songs.add(laul1)
playlist.songs.add(laul2)
#playlist.songs.add(laul3)
#playlist.songs.add(laul4)