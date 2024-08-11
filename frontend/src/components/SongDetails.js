import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchSongDetail } from '../services/api';
import { fetchArtistImages, fetchSongDetails } from '../services/spotifyAPI';
import { Oval } from 'react-loader-spinner';
import ArtistGraph from './ArtistGraph';
import '../css/SongDetails.css';

const SongDetail = () => {
    const { id } = useParams();
    const [songData, setSongData] = useState(null);
    const [songDetails, setSongDetails] = useState([]);
    const [artistImages, setArtistImages] = useState([]);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const getSongDetail = async () => {
            setLoading(true);
            try {
                const data = await fetchSongDetail(id);
                setSongData(data);

                // Fetch additional details for recommended songs
                if (data?.recommendedSongs?.length > 0) {
                    const details = await Promise.all(
                        data.recommendedSongs.map(song => fetchSongDetails(song))
                    );
                    setSongDetails(details);
                }

                // Fetch artist images
                if (data?.networkedArtistID?.length > 0) {
                    const images = await fetchArtistImages(data.networkedArtistID);
                    setArtistImages(images);
                }
            } catch (err) {
                setError('Failed to fetch song details.');
                console.error('Error fetching song details:', err);
            } finally {
                setLoading(false);
            }
        };

        getSongDetail();
    }, [id]);

    if (loading) {
        return (
            <div className="d-flex justify-content-center align-items-center loader-container">
                <Oval height={80} width={80} color="#123abc" ariaLabel="loading" />
            </div>
        );
    }

    if (error) {
        return <div className="alert alert-danger">{error}</div>;
    }

    if (!songData) {
        return null;
    }

    const { songName, networkedArtists } = songData;

    return (
        <div className="song-detail-container container mt-5">
            <h2 className="text-center song-detail-header">{songName}</h2>
            <div className="song-details">
                <p className="text-center"><strong>Recommended Songs</strong></p>
                <ul className="list-group">
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
                        <li className="list-group-item">No recommended songs found</li>
                    )}
                </ul>
                <p className="text-center"><strong>Networked Artists</strong></p>
                {networkedArtists?.length > 0 && (
                    <ArtistGraph artists={networkedArtists} artistImages={artistImages} />
                )}
            </div>
        </div>
    );
};

export default SongDetail;
