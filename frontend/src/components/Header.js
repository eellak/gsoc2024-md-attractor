import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import '../css/Header.css'; 

const Header = () => {
    const location = useLocation();

    return (
        <header className="header">
            <div className="container header-container">
                <h1 className="app-title">Song Recommendation App</h1>
                <nav className="nav-menu">
                    <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>
                        Home
                    </Link>
                    <Link to="/history" className={`nav-link ${location.pathname === '/history' ? 'active' : ''}`}>
                        History
                    </Link>
                </nav>
            </div>
        </header>
    );
};

export default Header;
