# core/views.py
import os
from django.shortcuts import render
from django.conf import settings

from rest_framework import generics
from .models import Video
from .serializers import VideoSerializer

# Extensões de vídeo suportadas no browser
SUPPORTED_EXTS = (".mp4", ".webm", ".ogg")

# --- API (DRF) ---
class VideoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class VideoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

# --- Vistas HTML ---
def index(request):
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    movies = [
        name for name in os.listdir(settings.MEDIA_ROOT)
        if name.lower().endswith(SUPPORTED_EXTS)
    ]
    movies.sort()
    return render(request, "index.html", {"movies": movies})

def play_movie(request, filename):
    # evitar path traversal (.. etc.)
    filename = os.path.basename(filename)
    return render(request, "play.html", {"filename": filename})