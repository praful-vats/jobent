// import React, { useState, useEffect } from 'react';
// import axios from 'axios';

// const ResumeList = () => {
//   const [resumes, setResumes] = useState([]);
//   const [jobDescription, setJobDescription] = useState('');
//   const [rewrittenResumes, setRewrittenResumes] = useState({});

//   useEffect(() => {
//     fetchResumes();
//   }, []);

//   const fetchResumes = async () => {
//     try {
//       const token = localStorage.getItem('token');
//       const response = await axios.get('http://localhost:8000/resume/api/resumes/', {
//         headers: {
//           'Authorization': `Token ${token}`,
//         },
//       });
//       setResumes(response.data);
//     } catch (error) {
//       console.error('Error fetching resumes:', error);
//     }
//   };

//   const handleRewrite = async (resumeId) => {
//     try {
//       const token = localStorage.getItem('token');
//       const response = await axios.put(`http://localhost:8000/resume/rewrite/${resumeId}/`, {
//         job_description: jobDescription,
//       }, {
//         headers: {
//           'Authorization': `Token ${token}`,
//         },
//       });
//       setRewrittenResumes((prev) => ({
//         ...prev,
//         [resumeId]: response.data.file_url, // Store the URL to the PDF file
//       }));
//       console.log('Resume rewritten:', response.data);
//     } catch (error) {
//       console.error('Error rewriting resume:', error);
//     }
//   };

//   return (
//     <div>
//       <h1>Resume List</h1>
//       <ul>
//         {resumes.length > 0 ? (
//           resumes.map((resume) => {
//             return (
//               <li key={resume.id}>
//                 <p>File: {resume.file_name}</p>
//                 <p>{resume.content}</p>
//                 {/* Job description input */}
//                 <textarea
//                   placeholder="Enter Job Description"
//                   onChange={(e) => setJobDescription(e.target.value)}
//                   style={{ width: "100%", height: "80px", marginBottom: "10px" }}
//                 />
//                 {/* Rewrite Resume button */}
//                 <button onClick={() => handleRewrite(resume.id)}>
//                   Rewrite Resume
//                 </button>
//                 {/* Display rewritten resume PDF */}
//                 {rewrittenResumes[resume.id] && (
//                   <div>
//                     <h3>Rewritten Resume</h3>
//                     <iframe 
//                       src={rewrittenResumes[resume.id]} 
//                       width="100%" 
//                       height="500px" 
//                       title="Rewritten Resume"
//                     />
//                   </div>
//                 )}
//               </li>
//             );
//           })
//         ) : (
//           <p>No resumes found. Upload one to get started!</p>
//         )}
//       </ul>
//     </div>
//   );
// };

// export default ResumeList;


import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './ResumeUpload.css';

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
      // const response = await axios.get('http://localhost:8000/resume/api/resumes/', {
      const BASE_URL = `${window.location.protocol}//${window.location.hostname}:8000`;
      const response = await axios.get(`${BASE_URL}/resume/api/resumes/`, {
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
      const BASE_URL = `${window.location.protocol}//${window.location.hostname}:8000`;
      const response = await axios.put
        (`${BASE_URL}/resume/rewrite/${resumeId}/`,
        {
          job_description: jobDescription,
        },
        {
          headers: {
            'Authorization': `Token ${token}`,
          },
        }
      );
      // Store the URL to the rewritten PDF
      setRewrittenResumes((prev) => ({
        ...prev,
        [resumeId]: response.data.file_url, // Assuming the response contains a URL to the rewritten resume PDF
      }));
      console.log('Resume rewritten:', response.data);
    } catch (error) {
      console.error('Error rewriting resume:', error);
    }
  };

  return (
    <div className="upload-resume-container">
      <h1>Recent Resume</h1>
      <ul>
        {resumes.length > 0 ? (
          resumes.map((resume) => (
            <li key={resume.id}>
              <p>File: {resume.file_name}</p>
              <p>{resume.content}</p>
              {/* Job description input */}
              <textarea 
                placeholder="enter job description"
                onChange={(e) => setJobDescription(e.target.value)}
                style={{
                  width: '100%',
                  height: '80px',
                  marginBottom: '10px',
                  backgroundColor: 'white',
                  color: 'black',
                  borderRadius: '5px'
                }}
                
              />
              {/* Rewrite Resume button */}
              <button className="submit-button" onClick={() => handleRewrite(resume.id)}>Rewrite Resume</button>

              {/* Display rewritten resume PDF */}
              {rewrittenResumes[resume.id] && (
                <div>
                  <h3>Rewritten Resume</h3>
                  <iframe
                    src={rewrittenResumes[resume.id]} // URL to the rewritten PDF
                    width="100%"
                    height="500px"
                    title="Rewritten Resume"
                    frameBorder="0"
                  />
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
