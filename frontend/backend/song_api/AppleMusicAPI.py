import os
from dotenv import load_dotenv
from typing import Dict, List, Optional, Tuple
import requests

load_dotenv()

class AppleMusicAPI():
    """
    A class that interacts with the Apple Music API to retrieve song details and related information.

    Attributes:
        developer_token (str): The Apple Music Developer Token.
        base_url (str): The base URL for Apple Music API.
        data (Dict[str, str]): A dictionary containing data for the song search.

    Methods:
        getSongDetails: Retrieves the details of a song based on the search query.
        collectGenres: Collects the genres of an artist.
        relatedArtists: Retrieves the related artists.
        getTopTracks: Retrieves the top tracks of collaborated artists.
    """

    def __init__(self, data: Dict[str, str]):
        self.developer_token: str = os.getenv('APPLE_MUSIC_DEVELOPER_TOKEN')
        self.base_url: str = "https://api.music.apple.com/v1/"
        self.data: Dict[str, str] = data

    def getSongDetails(self) -> Tuple[Optional[str], Optional[str], Optional[List[str]], Optional[str]]:
        """
        Retrieves the details of a song based on the search query.

        Returns:
            Tuple[Optional[str], Optional[str], Optional[List[str]], Optional[str]]: A tuple containing the song ID, song name, genres, and an error message if applicable.
        """
        track_name: str = self.data['search']
        url: str = f"{self.base_url}catalog/us/search"
        params = {
            "term": track_name,
            "types": "songs",
            "limit": 1
        }
        headers = {"Authorization": f"Bearer {self.developer_token}"}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            return None, None, None, "Error: Failed to fetch data from Apple Music API."

        results = response.json()
        if "results" not in results or "songs" not in results["results"]:
            return None, None, None, "Error: No song found with the given name."

        song_data = results["results"]["songs"]["data"][0]
        song_id: str = song_data["id"]
        song_name: str = song_data["attributes"]["name"]
        artist_id: str = song_data["relationships"]["artists"]["data"][0]["id"]

        genres = self.collectGenres(artist_id)
        return song_id, song_name, genres, None

    def collectGenres(self, artist_id: str) -> List[str]:
        """
        Collects the genres of an artist.

        Args:
            artist_id (str): The ID of the artist.

        Returns:
            List[str]: A list of genres associated with the artist.
        """
        url: str = f"{self.base_url}catalog/us/artists/{artist_id}"
        headers = {"Authorization": f"Bearer {self.developer_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return []

        artist_data = response.json()
        if "data" not in artist_data or len(artist_data["data"]) == 0:
            return []

        return artist_data["data"][0]["attributes"].get("genreNames", [])

    def relatedArtists(self, artist_id: str) -> List[Dict[str, str]]:
        """
        Retrieves the related artists.

        Args:
            artist_id (str): The ID of the artist.

        Returns:
            List[Dict[str, str]]: A list of related artists and their genres.
        """
        # Apple Music API may not provide "related artists" as directly as Spotify.
        # Implement a placeholder method or use a workaround if needed.
        return [{"id": artist_id, "name": "Related Artist Example"}]

    def getTopTracks(self, artist_id: str) -> List[Dict[str, str]]:
        """
        Retrieves the top tracks of an artist.

        Args:
            artist_id (str): The ID of the artist.

        Returns:
            List[Dict[str, str]]: A list of the artist's top tracks.
        """
        url: str = f"{self.base_url}catalog/us/artists/{artist_id}/top-songs"
        headers = {"Authorization": f"Bearer {self.developer_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            return []

        top_songs = response.json()
        if "data" not in top_songs:
            return []

        return [{"name": song["attributes"]["name"], "id": song["id"]} for song in top_songs["data"]]
