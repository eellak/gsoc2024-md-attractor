import React, { useState } from 'react';
import { fetchRecommendedSong } from '../services/api';
import { Oval } from 'react-loader-spinner'; 
import '../css/SongList.css';

const SongList = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [songs, setSongs] = useState([]);
    const [networkedArtists, setNetworkedArtists] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [searched, setSearched] = useState(false);

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
            } else {
                setSongs(data['Recommended Songs'] || []);
                setNetworkedArtists(data['Networked Artist'] || []);
                setError('');
            }
        } catch (err) {
            setError('An error occurred while fetching data.');
            setSongs([]);
            setNetworkedArtists([]);
        } finally {
            setLoading(false);
        }
    };

    const hasContent = searched || songs.length > 0 || networkedArtists.length > 0 || error;

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
                    <Oval
                        height={80}
                        width={80}
                        color="#123abc"
                        ariaLabel="loading"
                    />
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
                                    <li key={index} className="list-group-item">{artist}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </>
            )}
        </div>
    );
};

export default SongList;