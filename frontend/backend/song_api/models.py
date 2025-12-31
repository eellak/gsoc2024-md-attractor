from django.db import models
from django.utils import timezone

class Song(models.Model):
    songId = models.CharField(max_length=100, primary_key=True)
    songName = models.CharField(max_length=100)
    recommendedSongs = models.ManyToManyField('RecommendedSong')
    artistName = models.ManyToManyField('ArtistNetwork')
    dateCreated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.songName
    
class RecommendedSong(models.Model):
    songId = models.CharField(max_length=100, primary_key=True)
    songName = models.CharField(max_length=100)
    popularity = models.IntegerField(default=0)

    def __str__(self):
        return self.songId
    
class ArtistNetwork(models.Model):
    artistId = models.CharField(max_length=100, primary_key=True)
    artistName = models.CharField(max_length=100)

    def __str__(self):
        return self.artistName
