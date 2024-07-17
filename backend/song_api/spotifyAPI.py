import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from typing import Dict, List, Optional, Tuple

load_dotenv()

class SpotifyAPI():
    """
    A class that interacts with the Spotify API to retrieve song details and related information.

    Attributes:
        client_id (str): The client ID for the Spotify API.
        client_secret (str): The client secret for the Spotify API.
        sp (spotipy.Spotify): An instance of the spotipy.Spotify class for making API requests.
        data (Dict[str, str]): A dictionary containing data for the song search.

    Methods:
        getSongDetails: Retrieves the details of a song based on the search query.
        collectGenres: Collects the genres of an artist.
        relatedArtists: Retrieves the related artists and their genres.
        getTopTracks: Retrieves the top tracks of collaborated artists.
    """

    def __init__(self, data: Dict[str, str]):
        self.client_id: str = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret: str = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.sp: spotipy.Spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.client_id,client_secret=self.client_secret))
        self.data: Dict[str, str] = data

    def getSongDetails(self) -> Tuple[Optional[str], Optional[str], Optional[Dict[str, List[str]]], Optional[Dict[str, List[Dict[str, str]]]]]:
        """
        Retrieves the details of a song based on the search query.

        Returns:
            Tuple[Optional[str], Optional[str], Optional[Dict[str, List[str]]], Optional[Dict[str, List[Dict[str, str]]]]]: A tuple containing the song ID, song name, collaborated artists, and their top tracks.
        """
        trackName: str = self.data['search']
        results: Dict[str, Dict[str, List[Dict[str, str]]]] = self.sp.search(q='track:' + trackName, type='track')

        if not len(results['tracks']['items']):
            return None, None, None, "Error: No song found with the given name."

        self.songId: str = results['tracks']['items'][0]['id']
        self.songName: str = results['tracks']['items'][0]['name']

        self.artistDetails: List[Dict[str, str]] = results['tracks']['items'][0]['artists']
        self.artistID: str = self.artistDetails[0]['id']

        # Fetching the Genre of the Song
        self.genres: List[str] = self.collectGenres(self.artistID)

        # List of Artists, who had collaborated with the Primary artist
        self.collaboratedArtists: Dict[str, List[str]] = self.relatedArtists(self.artistID, self.genres)

        # for artists in self.collaboratedArtists:
        self.topTracks: Dict[str, List[Dict[str, str]]] = self.getTopTracks(self.collaboratedArtists)

        return self.songId, self.songName, self.collaboratedArtists, self.topTracks



    def collectGenres(self, artistID: str) -> List[str]:
        """
        Collects the genres of an artist.

        Args:
            artistID (str): The ID of the artist.

        Returns:
            List[str]: A list of genres associated with the artist.
        """
        result: Dict[str, List[str]] = self.sp.artist(artistID)
        genres: List[str] = result['genres']

        return genres
    


    def relatedArtists(self, artistID: str, genres: List[str]) -> Dict[str, List[str]]:
        """
        Retrieves the related artists and their genres.

        Args:
            artistID (str): The ID of the artist.
            genres (List[str]): A list of genres associated with the artist.

        Returns:
            Dict[str, List[str]]: A dictionary containing the related artists and their genres.
        """
        collaborations: Dict[str, List[str]] = {artistID: genres}
        results: Dict[str, List[Dict[str, str]]] = self.sp.artist_related_artists(artist_id = artistID)
        items: List[Dict[str, str]] = results['artists']

        for artist in items:
            collaborations[artist['id']] = artist['genres']

        return collaborations
    

    
    def getTopTracks(self, collaboratedArtists: Dict[str, List[str]]) -> Dict[str, List[Dict[str, str]]]:
        """
        Retrieves the top tracks of collaborated artists.

        Args:
            collaboratedArtists (Dict[str, List[str]]): A dictionary containing the collaborated artists and their genres.

        Returns:
            Dict[str, List[Dict[str, str]]]: A dictionary containing the collaborated artists and their top tracks.
        """
        topTracks: Dict[str, List[Dict[str, str]]] = {}
        for artistID in collaboratedArtists:
            results: Dict[str, List[Dict[str, str]]] = self.sp.artist_top_tracks(artist_id = artistID)
            currentArtistTopTracks: List[Dict[str, str]] = []
            for trackNumber in range(0, len(results['tracks'])):
                trackInfo: Dict[str, str] = {
                    'name': results['tracks'][trackNumber]['name'],
                    'id': results['tracks'][trackNumber]['id'],
                    'popularity': results['tracks'][trackNumber]['popularity']
                }
                currentArtistTopTracks.append(trackInfo)

            topTracks[artistID] = currentArtistTopTracks
        return topTracks
    

    def networkedArtist(self, artistsID: List[str]) -> List[str]:
        """
        Retrieves the names of the networked artists.

        Args:
            artistsID (List[str]): A list of artist IDs.

        Returns:
            List[str]: A list of names of the networked artists.
        """
        networkedArtist: List[str] = []
        for id in artistsID:
            result = self.sp.artist(id)
            networkedArtist.append(result['name'])

        return networkedArtist
