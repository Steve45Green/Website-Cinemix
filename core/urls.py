from django.urls import path
from .views import (
    index,
    play_movie,
    VideoListCreateAPIView,
    VideoRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # HTML
    path("", index, name="index"),
    path("play/<str:filename>/", play_movie, name="play_movie"),

    # API
    path("videos/", VideoListCreateAPIView.as_view(), name="video_list_create"),
    path("videos/<int:pk>/", VideoRetrieveUpdateDestroyAPIView.as_view(), name="video_detail"),
]
