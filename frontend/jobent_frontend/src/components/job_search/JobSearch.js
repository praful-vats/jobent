import React, { useState } from 'react';
import axios from 'axios';

const JobSearch = () => {
  const [matchedJobs, setMatchedJobs] = useState([]);

  const handleJobSearch = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('http://localhost:8000/resume/search_jobs/', {}, {
        headers: {
          'Authorization': `Token ${token}`,
        },
      });
      setMatchedJobs(response.data.matched_jobs);
    } catch (error) {
      console.error('Error searching for jobs:', error);
    }
  };

  return (
    <div>
      <h1>Job Search</h1>
      <button onClick={handleJobSearch}>Search for Jobs</button>
      <ul>
        {matchedJobs.length > 0 ? (
          matchedJobs.map((job, index) => (
            <li key={index}>
              <h2>{job.title}</h2>
              <p>{job.description}</p>
              <p>Similarity Score: {job.similarity_score.toFixed(2)}</p>
            </li>
          ))
        ) : (
          <p>No matched jobs found.</p>
        )}
      </ul>
    </div>
  );
};

export default JobSearch;