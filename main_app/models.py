from django.db import models
import time
from django.contrib.auth.models import User

# Create your models here.
# class User(models.Model):
#     username: models.CharField(max_)

class Artist(models.Model):

    name = models.CharField(max_length=100)
    img = models.CharField(max_length=500)
    bio = models.TextField(max_length=500)
    verified_artist = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # Here is our new column
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

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

# Playlist model
class Playlist(models.Model):

    title = models.CharField(max_length=150)
    # this is many-to-many field, this will create our join table
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.title