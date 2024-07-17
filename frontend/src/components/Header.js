import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => (
    <header className="bg-primary text-white py-3">
        <div className="container">
            <h1>Song Recommendation App</h1>
            <nav className="nav">
                <Link to="/" className="nav-link text-white">Home</Link>
                <Link to="/history" className="nav-link text-white">History</Link>
            </nav>
        </div>
    </header>
);

export default Header;
