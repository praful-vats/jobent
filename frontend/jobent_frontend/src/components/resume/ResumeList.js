import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ResumeList = () => {
  const [resumes, setResumes] = useState([]);
  const [jobDescription, setJobDescription] = useState('');
  const [rewrittenResumes, setRewrittenResumes] = useState({});

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/resume/api/resumes/', {
        headers: {
          'Authorization': `Token ${token}`,
        },
      });
      setResumes(response.data);
    } catch (error) {
      console.error('Error fetching resumes:', error);
    }
  };

  const handleRewrite = async (resumeId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.put(`http://localhost:8000/resume/rewrite/${resumeId}/`, {
        job_description: jobDescription,
      }, {
        headers: {
          'Authorization': `Token ${token}`,
        },
      });
      setRewrittenResumes((prev) => ({
        ...prev,
        [resumeId]: response.data.rewritten_resume,
      }));
      console.log('Resume rewritten:', response.data);
    } catch (error) {
      console.error('Error rewriting resume:', error);
    }
  };

  return (
    <div>
      <h1>Resume List</h1>
      <ul>
        {resumes.length > 0 ? (
          resumes.map((resume) => (
            <li key={resume.id}>
              <h2>{resume.name}</h2>
              <p>File: {resume.file_name}</p>
              <p>{resume.content}</p>
              {/* Job description input */}
              <textarea
                placeholder="Enter Job Description"
                onChange={(e) => setJobDescription(e.target.value)}
                style={{ width: "100%", height: "80px", marginBottom: "10px" }}
              />
              {/* Rewrite Resume button */}
              <button onClick={() => handleRewrite(resume.id)}>
                Rewrite Resume
              </button>
              {/* Display rewritten resume */}
              {rewrittenResumes[resume.id] && (
                <div>
                  <h3>Rewritten Resume</h3>
                  <p>{rewrittenResumes[resume.id]}</p>
                </div>
              )}
            </li>
          ))
        ) : (
          <p>No resumes found. Upload one to get started!</p>
        )}
      </ul>
    </div>
  );
};

export default ResumeList;