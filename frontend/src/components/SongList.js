import React, { useState, useEffect } from 'react';
import { fetchRecommendedSong } from '../services/api';
import { fetchArtistImages } from '../services/spotifyAPI';
import { Oval } from 'react-loader-spinner';
import '../css/SongList.css';
import ArtistGraph from './ArtistGraph';

const SongList = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [songs, setSongs] = useState([]);
    const [networkedArtists, setNetworkedArtists] = useState([]);
    const [networkedArtistsID, setNetworkedArtistsID] = useState([]);
    const [artistImages, setArtistImages] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [searched, setSearched] = useState(false);

    useEffect(() => {
        const fetchImages = async () => {
            if (networkedArtistsID.length > 0) {
                console.log('Fetching images for artist IDs:', networkedArtistsID);
                const images = await fetchArtistImages(networkedArtistsID);
                console.log('Received artist images:', images);
                setArtistImages(images);
            }
        };
        fetchImages();
    }, [networkedArtistsID]);

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
            <h2 className="text-center">Recommended Songs</h2>
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
            {error && <div className="alert alert-danger">{error}</div>}
            {loading ? (
                <div className="d-flex justify-content-center align-items-center loader-container">
                    <Oval height={80} width={80} color="#123abc" ariaLabel="loading" />
                </div>
            ) : (
                <>
                    {searched && (
                        <ul className="list-group mt-3">
                            {songs.length > 0 ? (
                                songs.map((song, index) => (
                                    <li key={index} className="list-group-item">{song}</li>
                                ))
                            ) : (
                                <li className="list-group-item">No songs found</li>
                            )}
                        </ul>
                    )}
                    {searched && networkedArtists.length > 0 && (
                        <div className="mt-4">
                            <h3 className="text-center">Networked Artists</h3>
                            <ul className="list-group mt-3">
                                {networkedArtists.map((artist, index) => (
                                    <li key={index} className="list-group-item">
                                        {artist}
                                        {artistImages[index] && artistImages[index].imageUrl && (
                                            <img 
                                                src={artistImages[index].imageUrl} 
                                                alt={artist} 
                                                style={{width: '50px', height: '50px', marginLeft: '10px'}}
                                                onError={(e) => {
                                                    console.error(`Failed to load image for ${artist}`);
                                                    e.target.src = 'https://via.placeholder.com/50';
                                                }}
                                            />
                                        )}
                                        {artistImages[index] && artistImages[index].error && (
                                            <span style={{color: 'red', marginLeft: '10px'}}>
                                                Error: {artistImages[index].error}
                                            </span>
                                        )}
                                    </li>
                                ))}
                            </ul>
                            <div className="mt-4">
                                <h3 className="text-center">Artist Network Graph</h3>
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