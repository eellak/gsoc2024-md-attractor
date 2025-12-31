from song_api import spotifyAPI
import networkx as nx
from typing import List, Dict, Tuple

import matplotlib.pyplot as plt

class ConstructGraph():
    """
    A class to construct a graph based on collaborated artists and calculate similarity between them.

    Attributes:
        collaboratedArtists (Dict[str, List[str]]): A dictionary containing collaborated artists and their genres.
        data (Dict[str, List[str]]): The collaborated artists and their genres.
        G (nx.Graph): The graph object to store the constructed graph.

    Methods:
        constructGraph(): Constructs the graph based on the collaborated artists and their genres.
        calculateSimilarity(genres1: List[str], genres2: List[str]) -> float: Calculates the similarity between two lists of genres.
        similarityComparison(threshold: float) -> List[Tuple[str, str, Dict[str, float]]]: Compares the similarity between artists and returns a list of filtered edges.
        extractArtists() -> List[str]: Extracts the artists from the filtered edges and returns a list of artists.
    """

    def __init__(self, collaboratedArtists: Dict[str, List[str]]) -> None:
        self.data = collaboratedArtists
        self.G = nx.Graph()
        self.constructGraph()
        self.similarityComparison(0.5)

    def constructGraph(self) -> None:
        """
        Constructs the graph based on the collaborated artists and their genres.
        """
        rootArtist = next(iter(self.data))
        self.G.add_node(rootArtist)

        for artist in self.data:
            if artist == rootArtist:
                continue
            self.G.add_node(artist)
            genres1 = self.data[rootArtist]
            genres2 = self.data[artist]

            similarity = self.calculateSimilarity(genres1, genres2)
            self.G.add_edge(rootArtist, artist, weight = similarity)

    def calculateSimilarity(self, genres1: List[str], genres2: List[str]) -> float:
        """
        Calculates the similarity between two lists of genres.

        Args:
            genres1 (List[str]): The first list of genres.
            genres2 (List[str]): The second list of genres.

        Returns:
            float: The similarity between the two lists of genres.
        """
        commonGenres = list(set(genres1) & set(genres2))
        similarity = len(commonGenres) / max(len(genres1), len(genres2))
        return similarity
    
    def similarityComparison(self, threshold: float) -> List[Tuple[str, str, Dict[str, float]]]:
        """
        Compares the similarity between artists and returns a list of filtered edges.

        Args:
            threshold (float): The threshold value for similarity.

        Returns:
            List[Tuple[str, str, Dict[str, float]]]: A list of filtered edges, where each edge is represented as a tuple containing the source artist, target artist, and a dictionary of attributes.
        """
        self.filteredEdges = []
        for edge in self.G.edges(data=True):
            if edge[2]['weight'] >= threshold:
                self.filteredEdges.append(edge)

        return self.filteredEdges
    
    def extractArtists(self) -> List[str]:
        """
        Extracts the artists from the filtered edges and returns a list of artists.

        Returns:
            List[str]: A list of artists.
        """
        artists = []
        for edge in self.filteredEdges:
            artists.append(edge[1])
        
        return artists
