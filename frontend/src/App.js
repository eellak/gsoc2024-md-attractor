import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import HistoryPage from './pages/HistoryPage';

const App = () => (
    <Router>
        <Header />
        <main className="py-4">
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/history" element={<HistoryPage />} />
            </Routes>
        </main>
    </Router>
);

export default App;
