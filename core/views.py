import os
from django.shortcuts import render
from django.conf import settings
SUPPORTED_EXTS = ('.mp4', '.webm', '.ogg')  # formatos mais seguros no browser

def index(request):
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    movies = []
    for name in os.listdir(settings.MEDIA_ROOT):
        if name.lower().endswith(SUPPORTED_EXTS):
            movies.append(name)
    movies.sort()
    return render(request, 'index.html', {'movies': movies})

def play_movie(request, filename):
    # evitar path traversal (.. etc.)
    filename = os.path.basename(filename)
    return render(request, 'play.html', {'filename': filename})