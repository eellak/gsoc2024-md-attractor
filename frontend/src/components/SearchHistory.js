import React, { useEffect, useState } from 'react';
import { fetchSearchHistory } from '../services/api';

const SearchHistory = () => {
    const [history, setHistory] = useState([]);
    const [error, setError] = useState('');

    useEffect(() => {
        const getHistory = async () => {
            try {
                const data = await fetchSearchHistory();
                setHistory(data);
            } catch (err) {
                setError('Failed to fetch search history.');
                console.error('Error fetching search history:', err);
            }
        };

        getHistory();
    }, []);

    return (
        <div className="container mt-5">
            <h2>Search History</h2>
            {error && <div className="alert alert-danger">{error}</div>}
            <ul className="list-group">
                {history.map((song, index) => (
                    <li key={index} className="list-group-item">
                        {song.songName} - {new Date(song.dateCreated).toLocaleString()}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default SearchHistory;
