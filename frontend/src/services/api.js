import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const fetchRecommendedSong = async (searchQuery) => {
    const response = await axios.post(`${API_URL}/`, { search: searchQuery });
    return response.data;
};

export const fetchSearchHistory = async () => {
    const response = await axios.get(`${API_URL}/history/`);
    return response.data;
};

export const fetchSongDetail = async (id) => {
    try {
        const response = await axios.get(`${API_URL}/song-detail/${id}/`);
        return response.data;
    } catch (error) {
        console.error('Error fetching song details:', error);
        throw error; // Rethrow to handle it in the component
    }
    
};