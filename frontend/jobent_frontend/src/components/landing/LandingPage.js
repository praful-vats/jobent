import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';

const LandingPage = () => {
    const navigate = useNavigate();

    return (
        <div className="container">
            {/* Navigation Bar */}
            <div className="nav">
                <div className="auth-buttons">
                    <button 
                        className="login-btn" 
                        onClick={() => navigate("/login")}
                    >
                        Login
                    </button>
                    <button 
                        className="signup-btn" 
                        onClick={() => navigate("/signup")}
                    >
                        Signup
                    </button>
                </div>
            </div>
            
            {/* Title */}
            <h1 className="title">Joƃent:</h1>
            
            {/* Cards Section */}
            <div className="cards-container">
                <div className="card">
                    <div className="icon">⊖</div>
                    <h2>Resume-focused</h2>
                    <p>
                        By leveraging AI service leverage efficient job search and effective job application process solutions.
                    </p>
                </div>

                <div className="card">
                    <div className="icon">↔</div>
                    <h2>System-driven</h2>
                    <p>
                        Deep understanding bot provide comprehensive services to effectivly communicate and manage interviews on your behalf.
                    </p>
                </div>

                <div className="card">
                    {/* <div className="icon3">☩</div> */}
                    <svg className="icon" width="51" height="52" viewBox="0 0 51 52" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M33.9815 42.8799L32.0369 40.9354L35.1129 37.8595L25.3901 28.1367L15.9149 37.612L18.9908 40.6879L17.0463 42.6324L8.94991 34.5361L10.8945 32.5915L13.9704 35.6674L23.4456 26.1922L13.7582 16.5048L10.6823 19.5807L8.73778 17.6362L16.8342 9.53982L18.7787 11.4844L15.7028 14.5603L25.3901 24.2476L35.325 14.3128L32.2491 11.2369L34.1936 9.29234L42.29 17.3887L40.3455 19.3333L37.2695 16.2573L27.3347 26.1922L37.0574 35.9149L40.1333 32.839L42.0779 34.7835L33.9815 42.8799Z" fill="black"/>
                    </svg>
                    <h2>Premium-factor</h2>
                    <p>
                        Premium features lets you stay ahead with tailored resume, cover letter and unlimited search.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default LandingPage;
