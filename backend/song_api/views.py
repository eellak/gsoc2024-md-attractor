from django.shortcuts import render
from rest_framework.response import Response
from song_api import models
from song_api import serializers
from rest_framework.decorators import api_view
from song_api import spotifyAPI
from song_api import egoNetwork
from django.http import JsonResponse
from song_api import serializers
from typing import List, Dict
from django.utils import timezone

# Create your views here.

@api_view(['POST'])
def trackDetails(request) -> Response:
    """
    Retrieve track details and return recommended songs.

    Args: 
        request (Request): The HTTP request object.

    Returns: 
        Response: The HTTP response object containing the recommended songs.

    Raises: 
        models.Song.DoesNotExist: If the requested song does not exist in the database.

    """
    if models.Song.objects.filter(songName=request.data['search']).exists():
        song = models.Song.objects.get(songName=request.data['search'])
        if (timezone.now() - song.dateCreated).days <= 7:
            serializer = serializers.SongSerializer(song)
            recommended_songs = song.recommendedSongs.all().order_by('-popularity')
            recommendation = [s.songName for s in recommended_songs]
            artistNetwork = song.artistName.all()
            networkedArtistData = [{"artistName": a.artistName, "artistId": a.artistId} for a in artistNetwork]
            networkedArtistName = [a['artistName'] for a in networkedArtistData][:11]
            networkedArtistID = [a['artistId'] for a in networkedArtistData][:11]
            return Response({"Recommended Songs": recommendation, "Song Name": song.songName, "Networked Artist": networkedArtistName[:11], "Networked Artist ID": networkedArtistID})
        else:
            spotifyInstance = spotifyAPI.SpotifyAPI(request.data)
            songId, songName, collaboratedArtists, topTracks = spotifyInstance.getSongDetails()

            if topTracks == "Error: No song found with the given name.":
                return Response({"Error": topTracks})

            graph = egoNetwork.ConstructGraph(collaboratedArtists)
            artistEgoNEtwork = graph.extractArtists()
            songPopularity = topTracksFromEgoNetwork(artistEgoNEtwork, topTracks)

            networkedArtistID = list(collaboratedArtists.keys())
            
            recommendedSongsName = [data['name'] for data in songPopularity][:10]
            recommendedSongsId = [data['id'] for data in songPopularity][:10]
            recommendedSongsPopularity = [data['popularity'] for data in songPopularity][:10]

            networkedArtistName = spotifyInstance.networkedArtist(networkedArtistID)

            song.songId = songId
            song.songName = songName
            song.dateCreated = timezone.now()
            song.save()

            song.recommendedSongs.clear()
            song.artistName.clear()

            for id, name, songPopularity in zip(recommendedSongsId, recommendedSongsName, recommendedSongsPopularity):
                if models.RecommendedSong.objects.filter(songId=id).exists(): 
                    suggestion = models.RecommendedSong.objects.get(songId=id)
                else:
                    suggestion = models.RecommendedSong.objects.create(songId=id, songName=name, popularity=songPopularity)
                    suggestion.save()
                song.recommendedSongs.add(suggestion)

            for artistID, artistName in zip(networkedArtistID, networkedArtistName):
                if models.ArtistNetwork.objects.filter(artistId=artistID).exists():
                    artist = models.ArtistNetwork.objects.get(artistId=artistID)
                else:
                    artist = models.ArtistNetwork.objects.create(artistId=artistID, artistName=artistName)
                    artist.save()
                song.artistName.add(artist)

            serializer = serializers.SongSerializer(song)
            recommended_songs = song.recommendedSongs.all().order_by('-popularity')
            recommendation = [s.songName for s in recommended_songs]

            networkedArtistName = networkedArtistName[:11]
            return Response({"Recommended Songs": recommendation, "Song Name": songName, "Networked Artist": networkedArtistName, "Networked Artist ID": networkedArtistID})

    else:
        spotifyInstance = spotifyAPI.SpotifyAPI(request.data)
        songId, songName, collaboratedArtists, topTracks = spotifyInstance.getSongDetails()

        if topTracks == "Error: No song found with the given name.":
            return Response({"Error": topTracks})
        graph = egoNetwork.ConstructGraph(collaboratedArtists)
        artistEgoNEtwork = graph.extractArtists()
        songPopularity = topTracksFromEgoNetwork(artistEgoNEtwork, topTracks)

        networkedArtistID = list(collaboratedArtists.keys())
        
        recommendedSongsName = [data['name'] for data in songPopularity][:10]
        recommendedSongsId = [data['id'] for data in songPopularity][:10]
        recommendedSongsPopularity = [data['popularity'] for data in songPopularity][:10]

        networkedArtistName = spotifyInstance.networkedArtist(networkedArtistID)

        if models.Song.objects.filter(songId = songId).exists():
            song = models.Song.objects.get(songId = songId)
            song.dateCreated = timezone.now()
            song.save()
        else:
            song = models.Song.objects.create(songId = songId, songName = songName)
        
        for id, name, songPopularity in zip(recommendedSongsId, recommendedSongsName, recommendedSongsPopularity):
            if models.RecommendedSong.objects.filter(songId=id).exists(): 
                suggestion = models.RecommendedSong.objects.get(songId=id)
            else:
                suggestion = models.RecommendedSong.objects.create(songId=id, songName=name, popularity=songPopularity)
                suggestion.save()
            song.recommendedSongs.add(suggestion)

        for artistID, artistName in zip(networkedArtistID, networkedArtistName):
            if models.ArtistNetwork.objects.filter(artistId=artistID).exists():
                artist = models.ArtistNetwork.objects.get(artistId=artistID)
            else:
                artist = models.ArtistNetwork.objects.create(artistId=artistID, artistName=artistName)
                artist.save()
            song.artistName.add(artist)

        serializer = serializers.SongSerializer(song)
        recommended_songs = song.recommendedSongs.all().order_by('-popularity')
        recommendation = [s.songName for s in recommended_songs]

        networkedArtistName = networkedArtistName[:11]
        return Response({"Recommended Songs": recommendation, "Song Name": songName, "Networked Artist": networkedArtistName, "Networked Artist ID": networkedArtistID})



@api_view(['GET'])
def searchHistory(request) -> Response:
    """
    Retrieve the search history of songs.

    This function retrieves all the songs from the database and returns them as a response.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: The HTTP response object containing the serialized data of all songs.

    """
    allSongs = models.Song.objects.all()
    serializer = serializers.SongSerializer(allSongs, many=True)
    return Response(serializer.data)



def topTracksFromEgoNetwork(artistNetwork: List[str], topTracks: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    """
    Returns a list of recommended tracks based on the artist network and their top tracks.

    Args:
        artistNetwork (List[str]): A list of artists in the network.
        topTracks (Dict[str, List[Dict[str, str]]]): A dictionary containing the top tracks for each artist.

    Returns:
        List[Dict[str, str]]: A list of recommended tracks sorted by popularity.
    """
    songList = []
    for artist in artistNetwork:
        songList.extend(topTracks[artist])

    recommendation = sorted(songList, key=lambda x: x['popularity'], reverse=True)
    return recommendation


@api_view(['GET'])
def songDetails(request, id: str) -> Response:
    """
    Retrieve details of a specific song by its ID.

    Parameters:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the song.

    Returns:
        Response: The HTTP response object containing the serialized data of the song.
    """
    try:
        song = models.Song.objects.get(songId=id)
    except models.Song.DoesNotExist:
        return Response({"Error": "Song not found"}, status=404)

    serializer = serializers.SongSerializer(song)
    recommended_songs = song.recommendedSongs.all().order_by('-popularity')
    recommendation = [s.songName for s in recommended_songs]
    artistNetwork = song.artistName.all()[:11]
    networkedArtistName = [a.artistName for a in artistNetwork]
    networkedArtistID = [a.artistId for a in artistNetwork]

    data = {
        "songName": song.songName,
        "recommendedSongs": recommendation,
        "networkedArtists": networkedArtistName,
        "networkedArtistID": networkedArtistID
    }
    return Response(data)