import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import HistoryPage from './pages/HistoryPage';
import SongDetailsPage from './pages/SongDetailsPage';

const App = () => (
    <Router>
        <Header />
        <main className="py-4">
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/history" element={<HistoryPage />} />
                <Route path="/song-detail/:id" element={<SongDetailsPage/>} />
            </Routes>
        </main>
    </Router>
);

export default App;
