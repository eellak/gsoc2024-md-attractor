import React from 'react';
import '../css/BackgroundBubbles.css';

const BackgroundBubbles = () => {
    const bubbles = Array.from({ length: 10 });

    return (
        <div className="bubbles">
            {bubbles.map((_, index) => (
                <div key={index} className="bubble"></div>
            ))}
        </div>
    );
};

export default BackgroundBubbles;
