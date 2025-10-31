from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Se forem ficheiros de vídeo locais (upload para /media/videos/)
    file = models.FileField(upload_to='videos/', blank=True, null=True)
    # Ou, se forem vídeos externos (YouTube/Vimeo), guarda o URL:
    url = models.URLField(blank=True)
    # Thumbnail opcional
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title