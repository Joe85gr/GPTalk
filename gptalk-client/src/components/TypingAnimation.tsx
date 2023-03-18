import React from 'react';
import './TypingAnimation.css';

 export const TypingAnimation: React.FC = () => {
    return (
        <div className="chat-bubble">
            <div className="typing">
                <div className="dot"></div>
                <div className="dot"></div>
                <div className="dot"></div>
            </div>
        </div>
    )
  }

