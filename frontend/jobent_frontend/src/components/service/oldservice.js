import React, { useState } from 'react';
import './ServicePage.css';
import ResumeUpload from '../resume/ResumeUpload';
import ResumeList from '../resume/ResumeList';
import JobSearch from '../job_search/JobSearch';

const ServicePage = () => {
  const [activePopup, setActivePopup] = useState(null);

  const closePopup = () => {
    setActivePopup(null);
  };

  return (
    <div className="service-page">
      <header>
        <h1>Identifont</h1>
      </header>
      <main>
        <div className="grid">
          <div className="card" onClick={() => setActivePopup('upload')}>
            <h2>Upload Resume</h2>
            <p>Upload and manage your resumes effortlessly.</p>
          </div>
          <div className="card" onClick={() => setActivePopup('list')}>
            <h2>List Resumes</h2>
            <p>View and modify your uploaded resumes.</p>
          </div>
          <div className="card" onClick={() => setActivePopup('search')}>
            <h2>Job Search</h2>
            <p>Find jobs that best match your profile.</p>
          </div>
        </div>
      </main>

      {/* Conditional rendering for popups */}
      {activePopup === 'upload' && (
        <div className="popup">
          <div className="popup-content">
            <button className="close-button" onClick={closePopup}>X</button>
            <ResumeUpload />
          </div>
        </div>
      )}

      {activePopup === 'list' && (
        <div className="popup">
          <div className="popup-content">
            <button className="close-button" onClick={closePopup}>X</button>
            <ResumeList />
          </div>
        </div>
      )}

      {activePopup === 'search' && (
        <div className="popup">
          <div className="popup-content">
            <button className="close-button" onClick={closePopup}>X</button>
            <JobSearch />
          </div>
        </div>
      )}
    </div>
  );
};

export default ServicePage;
