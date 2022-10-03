from django.db import models
import time

# Create your models here.
class Artist(models.Model):

    name = models.CharField(max_length=150)
    img = models.CharField(max_length=500, default="avatar.png")
    bio = models.TextField(max_length=1000)
    verified_artist = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

# below Artist Model

class Song(models.Model):

    title = models.CharField(max_length=150)
    length = models.IntegerField(default=0)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="songs")

    def __str__(self):
        return self.title

    def get_length(self):
        return time.strftime("%-M:%S", time.gmtime(self.length))