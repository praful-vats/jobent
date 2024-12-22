// import React, { useState } from 'react';
// import './ServicePage.css';
// import ResumeUpload from '../resume/ResumeUpload';
// import ResumeList from '../resume/ResumeList';
// import JobSearch from '../job_search/JobSearch';

// const ServicePage = () => {
//   const [activePopup, setActivePopup] = useState(null);

//   const closePopup = () => {
//     setActivePopup(null);
//   };

//   return (
//     <div className="service-page">
//       <main>
//         <div className="grid3">
//           <div className="card3">
//               <p>ƃ:</p>
//           </div>
//           <div className="card5"> 
//               <p>✺</p>
//           </div>
//           <div className="card4"> 
//               {/* <p>𓁈</p> */}
//               <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
//                 <circle cx="12" cy="8" r="4" />
//                 <path d="M12 14c-4.4 0-8 2.2-8 5v1h16v-1c0-2.8-3.6-5-8-5z" />
//               </svg>
//           </div>
//         </div>
//         <div className="grid">
//           <div className="card" onClick={() => setActivePopup('upload')}>
//           <div className="card-header">
//             <p className='card-header1'>FIND</p>
//             <svg className='card-header2' fill="none" height="44" viewBox="0 0 24 24" width="44" xmlns="http://www.w3.org/2000/svg"><path d="m18.5 15.5 3.5-3.5-3.5-3.5-.707.707 2.293 2.293h-18.086v1h18.086l-2.293 2.293z" fill="#000"/></svg>
//           </div>
//           <div className="card-body">
//             <p className='card-body-icon'>𓂀</p>
//             <p className='card-body-text'>upload your resume and unlock opportunities by finding jobs tailored to your unique skills and experience.</p>
//           </div>
//           </div>
//           <div className="card" onClick={() => setActivePopup('list')}>
//           <div className="card-header">
//             <p className='card-header1'>GENERATE</p>
//             <svg className='card-header2' fill="none" height="44" viewBox="0 0 24 24" width="44" xmlns="http://www.w3.org/2000/svg"><path d="m18.5 15.5 3.5-3.5-3.5-3.5-.707.707 2.293 2.293h-18.086v1h18.086l-2.293 2.293z" fill="#000"/></svg>
//           </div>
//           <div className="card-body">
//             <p className='card-body-icon'>𓐌</p>
//             <p className='card-body-text'>generate customized resume and cover letters by analyzing the resume, job description, company website, and other public information.</p>
//           </div>
//           </div>
//           <div className="card" onClick={() => setActivePopup('search')}>
//           <div className="card-header">
//             <p className='card-header1'>BOT</p>
//             <svg className='card-header2' fill="none" height="44" viewBox="0 0 24 24" width="44" xmlns="http://www.w3.org/2000/svg"><path d="m18.5 15.5 3.5-3.5-3.5-3.5-.707.707 2.293 2.293h-18.086v1h18.086l-2.293 2.293z" fill="#000"/></svg>
//           </div>
//           <div className="card-body">
//             <p className='card-body-icon'>𓀨</p>
//             <p className='card-body-text'> listener bot can convert audio to text for use in the thank you letters and manage any follow-up actions like scheduling further interviews.</p>
//           </div>
//           </div>
//           <div className="card" onClick={() => setActivePopup('search')}>
//           <div className="card-header">
//             <p className='card-header1'>DATA</p>
//             <svg className='card-header2' fill="none" height="44" viewBox="0 0 24 24" width="44" xmlns="http://www.w3.org/2000/svg"><path d="m18.5 15.5 3.5-3.5-3.5-3.5-.707.707 2.293 2.293h-18.086v1h18.086l-2.293 2.293z" fill="#000"/></svg>
//           </div>
//           <div className="card-body">
//             <p className='card-body-icon'>░</p>
//             <p className='card-body-text'>comprehensive summary of your career data, to track seamless job matching and ensure alignment with the most relevant opportunities</p>
//           </div>
//           </div>
//         </div>
//         <div className="grid2">
//           <div className="card2" onClick={() => setActivePopup('search')}>
//             <div className="card-header">
//               <p className='card-header1'>CONVERSATION</p>
//               <svg className='card-header2' fill="none" height="44" viewBox="0 0 24 24" width="44" xmlns="http://www.w3.org/2000/svg"><path d="m18.5 15.5 3.5-3.5-3.5-3.5-.707.707 2.293 2.293h-18.086v1h18.086l-2.293 2.293z" fill="#000"/></svg>
//             </div>
//             <div className="card-body">
//               <p className='card-body-icon'>𓁨</p>
//               <p className='card-body-text'>generate customized resume and cover letters by analyzing the resume, job description, company website, and other public information.</p>
//             </div>
//           </div>
//           <div className="card2" onClick={() => setActivePopup('calender')}>
//             <div className="card-header">
//               <p className='card-header1'>CALENDER</p>
//               <svg className='card-header2' fill="none" height="44" viewBox="0 0 24 24" width="44" xmlns="http://www.w3.org/2000/svg"><path d="m18.5 15.5 3.5-3.5-3.5-3.5-.707.707 2.293 2.293h-18.086v1h18.086l-2.293 2.293z" fill="#000"/></svg>
//             </div>
//             <div className="card-body">
//               <p className='card-body-icon'>𓎎</p>
//               <p className='card-body-text'>generate customized resume and cover letters by analyzing the resume, job description, company website, and other public information.</p>
//             </div>
//           </div>
//         </div>
//       </main>

//       {/* Conditional rendering for popups */}
//       {activePopup === 'upload' && (
//         <div className="popup">
//           <div className="popup-content">
//             <button className="close-button" onClick={closePopup}>X</button>
//             <ResumeUpload />
//           </div>
//         </div>
//       )}

//       {activePopup === 'list' && (
//         <div className="popup">
//           <div className="popup-content">
//             <button className="close-button" onClick={closePopup}>X</button>
//             <ResumeList />
//           </div>
//         </div>
//       )}

//       {activePopup === 'search' && (
//         <div className="popup">
//           <div className="popup-content">
//             <button className="close-button" onClick={closePopup}>X</button>
//             <JobSearch />
//           </div>
//         </div>
//       )}
//     </div>
//   );
// };

// export default ServicePage;

import React, { useState, useEffect } from 'react';
import './ServicePage.css';
import { InlineWidget } from "react-calendly";
import ResumeUpload from '../resume/ResumeUpload';
import ResumeList from '../resume/ResumeList';
import JobSearch from '../job_search/JobSearch';
import axios from 'axios';

const ServicePage = () => {
  const [activePopup, setActivePopup] = useState(null);
  const [recentResumes, setRecentResumes] = useState([]);
  const [selectedResumeId, setSelectedResumeId] = useState(null);
  const [jobSearchResults, setJobSearchResults] = useState([]);

  const closePopup = () => {
    setActivePopup(null);
  };

  const fetchRecentResumes = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/resume/api/resumes/', {
        headers: {
          'Authorization': `Token ${token}`,
        },
      });
      setRecentResumes(response.data);
    } catch (error) {
      console.error('Error fetching recent resumes:', error);
    }
  };

  const handleJobSearch = async () => {
    console.log("Triggering job search...");
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('http://localhost:8000/resume/match-jobs/', { resume_id: selectedResumeId }, {
        headers: {
          'Authorization': `Token ${token}`,
        },
      });
      console.log("Response data:", response.data);
      setJobSearchResults(response.data.matched_jobs);
      console.log('Job search completed:', response.data.matched_jobs);
    } catch (error) {
      console.error('Error searching for jobs:', error);
    }
  };

  useEffect(() => {
    if (activePopup === 'upload') {
      fetchRecentResumes();
    }
  }, [activePopup]);

  return (
    <div className="service-page">
      <main>
        <div className="grid3">
          <div className="card3">
            <p>ƃ:</p>
          </div>
          <div className="card5"> 
            <p>✺</p>
          </div>
          <div className="card4"> 
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
              <circle cx="12" cy="8" r="4" />
              <path d="M12 14c-4.4 0-8 2.2-8 5v1h16v-1c0-2.8-3.6-5-8-5z" />
            </svg>
          </div>
        </div>
        <div className="grid">
          <div className="card" onClick={() => setActivePopup('upload')}>
            <div className="card-header">
              <p className="card-header1">FIND</p>
              <svg className="card-header2" fill="none" height="44" viewBox="0 0 24 24" width="44" xmlns="http://www.w3.org/2000/svg">
                <path d="m18.5 15.5 3.5-3.5-3.5-3.5-.707.707 2.293 2.293h-18.086v1h18.086l-2.293 2.293z" fill="#000"/>
              </svg>
            </div>
            <div className="card-body">
              <p className="card-body-icon">𓂀</p>
              <p className="card-body-text">Upload your resume and unlock opportunities by finding jobs tailored to your unique skills and experience.</p>
            </div>
          </div>
          <div className="card" onClick={() => setActivePopup('list')}>
            <div className="card-header">
              <p className="card-header1">GENERATE</p>
              <svg className="card-header2" fill="none" height="44" viewBox="0 0 24 24" width="44" xmlns="http://www.w3.org/2000/svg">
                <path d="m18.5 15.5 3.5-3.5-3.5-3.5-.707.707 2.293 2.293h-18.086v1h18.086l-2.293 2.293z" fill="#000"/>
              </svg>
            </div>
            <div className="card-body">
              <p className="card-body-icon">𓐌</p>
              <p className="card-body-text">Generate customized resume and cover letters by analyzing the resume, job description, company website, and other public information.</p>
            </div>
          </div>
          <div className="card" onClick={() => setActivePopup('search')}>
            <div className="card-header">
              <p className="card-header1">BOT</p>
              <svg className="card-header2" fill="none" height="44" viewBox="0 0 24 24" width="44" xmlns="http://www.w3.org/2000/svg">
                <path d="m18.5 15.5 3.5-3.5-3.5-3.5-.707.707 2.293 2.293h-18.086v1h18.086l-2.293 2.293z" fill="#000"/>
              </svg>
            </div>
            <div className="card-body">
              <p className="card-body-icon">𓀨</p>
              <p className="card-body-text">Listener bot can convert audio to text for use in the thank you letters and manage any follow-up actions like scheduling further interviews.</p>
            </div>
          </div>
          <div className="card" onClick={() => setActivePopup('search')}>
            <div className="card-header">
              <p className="card-header1">DATA</p>
              <svg className="card-header2" fill="none" height="44" viewBox="0 0 24 24" width="44" xmlns="http://www.w3.org/2000/svg">
                <path d="m18.5 15.5 3.5-3.5-3.5-3.5-.707.707 2.293 2.293h-18.086v1h18.086l-2.293 2.293z" fill="#000"/>
              </svg>
            </div>
            <div className="card-body">
              <p className="card-body-icon">░</p>
              <p className="card-body-text">Comprehensive summary of your career data, to track seamless job matching and ensure alignment with the most relevant opportunities.</p>
            </div>
          </div>
        </div>
        <div className="grid2">
          <div className="card2" onClick={() => setActivePopup('search')}>
            <div className="card-header">
              <p className='card-header1'>CONVERSATION</p>
              <svg className='card-header2' fill="none" height="44" viewBox="0 0 24 24" width="44" xmlns="http://www.w3.org/2000/svg"><path d="m18.5 15.5 3.5-3.5-3.5-3.5-.707.707 2.293 2.293h-18.086v1h18.086l-2.293 2.293z" fill="#000"/></svg>
            </div>
            <div className="card-body">
              <p className='card-body-icon'>𓁨</p>
              <p className='card-body-text'>generate customized resume and cover letters by analyzing the resume, job description, company website, and other public information.</p>
            </div>
          </div>
          <div className="card2" onClick={() => setActivePopup('calender')}>
            <div className="card-header">
              <p className="card-header1">CALENDAR</p>
              <svg className="card-header2" fill="none" height="44" viewBox="0 0 24 24" width="44" xmlns="http://www.w3.org/2000/svg">
                <path d="m18.5 15.5 3.5-3.5-3.5-3.5-.707.707 2.293 2.293h-18.086v1h18.086l-2.293 2.293z" fill="#000"/>
              </svg>
            </div>
            <div className="card-body">
              <p className="card-body-icon">𓎎</p>
              <p className="card-body-text">Generate customized resume and cover letters by analyzing the resume, job description, company website, and other public information.</p>
            </div>
          </div>
        </div>
      </main>

      {/* Conditional rendering for popups */}
      {/* {activePopup === 'upload' && (
        <div className="popup">
          <div className="popup-content">
            <button className="close-button" onClick={closePopup}>X</button>
            <ResumeUpload onUploadSuccess={() => { 
                fetchRecentResumes(); 
                handleJobSearch(); 
            }} />


            <h3>Recent Resumes</h3>
            <ul>
              {recentResumes.map((resume) => (
                <li key={resume.id}>{resume.file_name}</li>
              ))}
            </ul>
          </div>
        </div>
      )} */}

        {activePopup === 'upload' && (
          <div className="popup">
            <div className="popup-content">
              <button className="close-button" onClick={closePopup}>X</button>
              <ResumeUpload
                onUploadSuccess={(newResume) => {
                  fetchRecentResumes();
                  setSelectedResumeId(newResume.id); 
                }}
              />
              <h3>Select a Recent Resume</h3>
              <ul>
                {recentResumes.map((resume) => (
                  <li key={resume.id}>
                    <input
                      type="radio"
                      id={`resume-${resume.id}`}
                      name="resume"
                      value={resume.id}
                      onChange={() => setSelectedResumeId(resume.id)}
                    />
                    <label htmlFor={`resume-${resume.id}`}>{resume.file_name}</label>
                  </li>
                ))}
              </ul>
              <button onClick={handleJobSearch} disabled={!selectedResumeId}>
                Find Matching Jobs
              </button>
            </div>
          </div>
        )}

      {jobSearchResults.length > 0 && (
        <div className="job-search-results">
          <h2>Matched Jobs</h2>
          <ul>
            {jobSearchResults.map((job, index) => (
              <li key={index}>
                <h3>{job.title}</h3>
                <p>{job.description}</p>
                <p>Similarity Score: {job.similarity_score.toFixed(2)}</p>
              </li>
            ))}
          </ul>
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
            <JobSearch onJobSearchResults={(results) => setJobSearchResults(results)} />
          </div>
        </div>
      )}

      {activePopup === 'calender' && (
        <div className="popup">
          <div className="popup-content">
            <button className="close-button" onClick={closePopup}>X</button>
            <InlineWidget url="https://calendly.com/dodooed-13/30min" />
          </div>
        </div>
      )}
    </div>
  );
};

export default ServicePage;
