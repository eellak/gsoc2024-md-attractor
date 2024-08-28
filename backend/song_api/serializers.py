from rest_framework import serializers
from rest_framework.serializers import Serializer
from song_api import models

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Song
        fields = ['songId', 'songName', 'recommendedSongs', 'dateCreated']

class RecommendedSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RecommendedSong
        fields = ['songId', 'songName', 'popularity']
