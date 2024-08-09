import React, { useState, useEffect } from 'react';
import { fetchRecommendedSong } from '../services/api';
import { fetchArtistImages, fetchSongDetails } from '../services/spotifyAPI';
import { Oval } from 'react-loader-spinner';
import '../css/SongList.css';
import ArtistGraph from './ArtistGraph';

const SongList = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [songName, setSongName] = useState('');
    const [songs, setSongs] = useState([]);
    const [songDetails, setSongDetails] = useState([]);
    const [networkedArtists, setNetworkedArtists] = useState([]);
    const [networkedArtistsID, setNetworkedArtistsID] = useState([]);
    const [artistImages, setArtistImages] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [searched, setSearched] = useState(false);

    useEffect(() => {
        const fetchImages = async () => {
            if (networkedArtistsID.length > 0) {
                const images = await fetchArtistImages(networkedArtistsID);
                setArtistImages(images);
            }
        };
        fetchImages();
    }, [networkedArtistsID]);

    useEffect(() => {
        const fetchDetails = async () => {
            if (songs.length > 0) {
                const details = await Promise.all(
                    songs.map(song => fetchSongDetails(song))
                );
                setSongDetails(details);
            }
        };
        fetchDetails();
    }, [songs]);

    const handleSearch = async (e) => {
        e.preventDefault();
        setLoading(true);
        setSearched(true);
        try {
            const data = await fetchRecommendedSong(searchQuery);
            if (data.Error) {
                setError(data.Error);
                setSongs([]);
                setNetworkedArtists([]);
                setNetworkedArtistsID([]);
                setArtistImages([]);
            } else {
                setSongName(data['Song Name']);
                setSongs(data['Recommended Songs'] || []);
                setNetworkedArtists(data['Networked Artist'] || []);
                setNetworkedArtistsID(data['Networked Artist ID'] || []);
                setError('');
            }
        } catch (err) {
            setError('An error occurred while fetching data.');
            setSongs([]);
            setNetworkedArtists([]);
            setNetworkedArtistsID([]);
            setArtistImages([]);
        } finally {
            setLoading(false);
        }
    };

    const hasContent = searched || songs.length > 0 || networkedArtists.length > 0 || networkedArtistsID.length > 0 || error;

    return (
        <div className={`song-list-container container mt-5 ${hasContent ? 'has-content' : ''}`}>
            <h2 className="text-center">RECOMMENDED SONGS</h2>
            <form onSubmit={handleSearch} className="mb-3 search-form">
                <div className="input-group">
                    <input
                        type="text"
                        className="form-control"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="Enter Song Name"
                    />
                    <button type="submit" className="btn btn-primary">Search</button>
                </div>
            </form>
            {songName && <h3 className="text-center">{songName}</h3>}
            {error && <div className="alert alert-danger">{error}</div>}
            {loading ? (
                <div className="d-flex justify-content-center align-items-center loader-container">
                    <Oval height={80} width={80} color="#123abc" ariaLabel="loading" />
                </div>
            ) : (
                <>
                    {searched && (
                        <ul className="list-group mt-3">
                            {songDetails.length > 0 ? (
                                songDetails.map((song, index) => (
                                    <li key={index} className="list-group-item song-item">
                                        <a href={song.spotifyUrl} target="_blank" rel="noopener noreferrer" className="song-link">
                                            <img src={song.image} alt={song.name} className="song-image" />
                                            {song.name}
                                        </a>
                                    </li>
                                ))
                            ) : (
                                <li className="list-group-item">No songs found</li>
                            )}
                        </ul>
                    )}
                    {searched && networkedArtists.length > 0 && (
                        <div className="mt-4">
                            <div className="mt-4">
                                <h3 className="text-center">NETWORKED ARTIST GRAPH</h3>
                                <ArtistGraph artists={networkedArtists} artistImages={artistImages} />
                            </div>
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default SongList;
