import os
from django.shortcuts import render
from django.conf import settings

def index(request):
    # Lista todos os ficheiros na pasta media
    files = os.listdir(settings.MEDIA_ROOT)
    movies = [f for f in files if f.endswith(('.mp4', '.mkv', '.avi'))]
    return render(request, 'index.html', {'movies': movies})

def play_movie(request, filename):
    return render(request, 'play.html', {'filename': filename})