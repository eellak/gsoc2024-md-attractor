import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
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

  const sortedHistory = history.sort((a, b) => new Date(b.dateCreated) - new Date(a.dateCreated));

  return (
    <div className="search-history-container container mt-5">
      <h2 className="text-center search-history-header">Search History</h2>
      {error && <div className="alert alert-danger">{error}</div>}
      <ul className="list-group">
        {sortedHistory.map((song, index) => (
          <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
            <Link to={`/song-detail/${song.songId}`}>
              <span>{song.songName}</span>
            </Link>
            <span className="text-muted">{new Date(song.dateCreated).toLocaleString()}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SearchHistory;
