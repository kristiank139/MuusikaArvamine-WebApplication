from django.shortcuts import render

# Create your views here.

def play_song(request): # Sellest peaks tulema funktsioon, mis mängib laulu, kui front-endis vajutatakse "Mängi" nuppu
    if request.POST:
        print("Song played")
    return render(request, "game/game.html")