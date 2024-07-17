import React, { useState } from 'react';
import { fetchRecommendedSong } from '../services/api';

const SongList = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [songs, setSongs] = useState([]);
    const [networkedArtists, setNetworkedArtists] = useState([]);
    const [error, setError] = useState('');

    const handleSearch = async (e) => {
        e.preventDefault();
        try {
            const data = await fetchRecommendedSong(searchQuery);
            if (data.Error) {
                setError(data.Error);
                setSongs([]);
                setNetworkedArtists([]);
            } else {
                setSongs(data['Recommended Songs']);
                setNetworkedArtists(data['Networked Artist']);
                setError('');
            }
        } catch (err) {
            setError('An error occurred while fetching data.');
        }
    };

    return (
        <div className="container mt-5">
            <h2>Recommended Songs</h2>
            <form onSubmit={handleSearch} className="mb-3">
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
            <ul className="list-group">
                {songs.map((song, index) => (
                    <li key={index} className="list-group-item">{song}</li>
                ))}
            </ul>
            {networkedArtists.length > 0 && (
                <div className="mt-4">
                    <h3>Networked Artists</h3>
                    <ul className="list-group">
                        {networkedArtists.map((artist, index) => (
                            <li key={index} className="list-group-item">{artist}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default SongList;
