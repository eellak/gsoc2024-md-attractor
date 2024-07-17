from django.contrib import admin
from song_api import models
# Register your models here.

admin.site.register(models.Song)
admin.site.register(models.RecommendedSong)
admin.site.register(models.ArtistNetwork)
