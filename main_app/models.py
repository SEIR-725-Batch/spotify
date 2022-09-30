from django.db import models

# Create your models here.
class Artist(models.Model):

    name = models.CharField(max_length=150)
    img = models.CharField(max_length=500)
    bio = models.TextField(max_length=1000)
    verified_artist = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']