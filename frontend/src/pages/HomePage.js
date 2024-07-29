import React from 'react';
import SongList from '../components/SongList';
import BackgroundBubbles from '../components/BackgroundBubbles';

const HomePage = () => (
    <div className="home-page container">
        <BackgroundBubbles />
        <SongList />
    </div>
);

export default HomePage;
