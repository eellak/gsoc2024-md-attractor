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
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

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
    all_songs = models.Song.objects.all()
    song_names = [song.songName for song in all_songs]
    search_query = request.data['search']
    matched_song, score = process.extractOne(search_query, song_names, scorer=fuzz.token_set_ratio)

    if score >= 80:
        return handle_existing_song(matched_song, request.data)
    else:
        return handle_new_song(search_query, request.data)


def handle_existing_song(matched_song, request_data):
    try:
        song = models.Song.objects.get(songName=matched_song)
    except models.Song.DoesNotExist:
        return Response({"Error": "Song does not exist."})

    if (timezone.now() - song.dateCreated).days <= 7:
        return get_recommendations_for_existing_song(song)
    else:
        return update_song_details_from_spotify(song, request_data)


def handle_new_song(search_query, request_data):
    spotify_instance = spotifyAPI.SpotifyAPI(request_data)
    song_id, song_name, collaborated_artists, top_tracks = spotify_instance.getSongDetails()

    if top_tracks == "Error: No song found with the given name.":
        return Response({"Error": top_tracks})

    return create_new_song_entry(song_id, song_name, collaborated_artists, top_tracks)


def get_recommendations_for_existing_song(song):
    serializer = serializers.SongSerializer(song)
    recommended_songs = song.recommendedSongs.all().order_by('-popularity')
    recommendation = [s.songName for s in recommended_songs]

    artist_network = song.artistName.all()
    networked_artist_data = [
        {"artistName": a.artistName, "artistId": a.artistId} for a in artist_network
    ]
    networked_artist_name = [a['artistName'] for a in networked_artist_data][:11]
    networked_artist_id = [a['artistId'] for a in networked_artist_data][:11]

    return Response({
        "Recommended Songs": recommendation,
        "Song Name": song.songName,
        "Networked Artist": networked_artist_name,
        "Networked Artist ID": networked_artist_id
    })


def update_song_details_from_spotify(song, request_data):
    spotify_instance = spotifyAPI.SpotifyAPI(request_data)
    song_id, song_name, collaborated_artists, top_tracks = spotify_instance.getSongDetails()

    if top_tracks == "Error: No song found with the given name.":
        return Response({"Error": top_tracks})

    update_song_and_related_models(song, song_id, song_name, collaborated_artists, top_tracks)
    return get_recommendations_for_existing_song(song)


def create_new_song_entry(song_id, song_name, collaborated_artists, top_tracks):
    graph = egoNetwork.ConstructGraph(collaborated_artists)
    artist_ego_network = graph.extractArtists()
    song_popularity = topTracksFromEgoNetwork(artist_ego_network, top_tracks)

    networked_artist_id = list(collaborated_artists.keys())
    recommended_songs_name = [data['name'] for data in song_popularity][:10]
    recommended_songs_id = [data['id'] for data in song_popularity][:10]
    recommended_songs_popularity = [data['popularity'] for data in song_popularity][:10]

    spotify_instance = spotifyAPI.SpotifyAPI({})
    networked_artist_name = spotify_instance.networkedArtist(networked_artist_id)

    song, created = models.Song.objects.get_or_create(
        songId=song_id,
        defaults={'songName': song_name}
    )
    song.dateCreated = timezone.now()
    song.save()

    update_song_recommendations_and_artists(song, recommended_songs_id, recommended_songs_name, recommended_songs_popularity, networked_artist_id, networked_artist_name)

    return get_recommendations_for_existing_song(song)


def update_song_and_related_models(song, song_id, song_name, collaborated_artists, top_tracks):
    graph = egoNetwork.ConstructGraph(collaborated_artists)
    artist_ego_network = graph.extractArtists()
    song_popularity = topTracksFromEgoNetwork(artist_ego_network, top_tracks)

    networked_artist_id = list(collaborated_artists.keys())
    recommended_songs_name = [data['name'] for data in song_popularity][:10]
    recommended_songs_id = [data['id'] for data in song_popularity][:10]
    recommended_songs_popularity = [data['popularity'] for data in song_popularity][:10]

    spotify_instance = spotifyAPI.SpotifyAPI({})
    networked_artist_name = spotify_instance.networkedArtist(networked_artist_id)

    song.songId = song_id
    song.songName = song_name
    song.dateCreated = timezone.now()
    song.save()

    song.recommendedSongs.clear()
    song.artistName.clear()

    update_song_recommendations_and_artists(song, recommended_songs_id, recommended_songs_name, recommended_songs_popularity, networked_artist_id, networked_artist_name)


def update_song_recommendations_and_artists(song, recommended_songs_id, recommended_songs_name, recommended_songs_popularity, networked_artist_id, networked_artist_name):
    for id, name, popularity in zip(recommended_songs_id, recommended_songs_name, recommended_songs_popularity):
        suggestion, created = models.RecommendedSong.objects.get_or_create(
            songId=id,
            defaults={'songName': name, 'popularity': popularity}
        )
        song.recommendedSongs.add(suggestion)

    for artist_id, artist_name in zip(networked_artist_id, networked_artist_name):
        artist, created = models.ArtistNetwork.objects.get_or_create(
            artistId=artist_id,
            defaults={'artistName': artist_name}
        )
        song.artistName.add(artist)


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