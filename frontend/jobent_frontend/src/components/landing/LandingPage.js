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
            <h1 className="title">Jobent:</h1>
            
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
                    <div className="icon">X</div>
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
