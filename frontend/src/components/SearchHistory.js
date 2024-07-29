import React, { useEffect, useState } from 'react';
import { fetchSearchHistory } from '../services/api';
import '../css/SearchHistory.css';

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
        <div className="search-history-container container mt-5">
            <h2 className="text-center search-history-header">Search History</h2>
            {error && <div className="alert alert-danger">{error}</div>}
            <ul className="list-group">
                {history.map((song, index) => (
                    <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
                        <span>{song.songName}</span>
                        <span className="text-muted">{new Date(song.dateCreated).toLocaleString()}</span>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default SearchHistory;
