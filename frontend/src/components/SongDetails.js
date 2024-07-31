import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchSongDetail } from '../services/api';
import '../css/SongDetails.css';

const SongDetail = () => {
  const { id } = useParams();
  const [songData, setSongData] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const getSongDetail = async () => {
      try {
        const data = await fetchSongDetail(id);
        setSongData(data);
      } catch (err) {
        setError('Failed to fetch song details.');
        console.error('Error fetching song details:', err);
      }
    };

    getSongDetail();
  }, [id]);

  if (error) {
    return <div className="alert alert-danger">{error}</div>;
  }

  if (!songData) {
    return <div>Loading...</div>;
  }

  const { songName, recommendedSongs, networkedArtists } = songData;

  return (
    <div className="song-detail-container container mt-5">
      <h2 className="text-center song-detail-header">{songName}</h2>
      <div className="song-details">
        <p className='text-center'><strong>RECOMMENDED SONGS</strong></p>
        <ul>
          {recommendedSongs.map((song, index) => (
            <li key={index}>{song}</li>
          ))}
        </ul>
        <p className='text-center'><strong>NETWORKED ARTISTS</strong></p>
        <ul>
          {networkedArtists.map((artist, index) => (
            <li key={index}>{artist}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default SongDetail;
