// import React, { useState } from 'react';
// import axios from 'axios';
// import './ResumeUpload.css';

// const ResumeUpload = ({ onUploadSuccess }) => {
//   const [file, setFile] = useState(null);
//   const [filePreview, setFilePreview] = useState(null);
//   const [message, setMessage] = useState('');

//   const handleFileChange = (e) => {
//     const selectedFile = e.target.files[0];
//     if (selectedFile && selectedFile.type === 'application/pdf') {
//       setFile(selectedFile);

//       // Create a FileReader instance to read the file as a Data URL
//       const reader = new FileReader();
//       reader.onloadend = () => {
//         setFilePreview(reader.result); // Set the PDF preview
//       };
//       reader.readAsDataURL(selectedFile); // Read the file as a Data URL
//     } else {
//       setMessage('Please select a valid PDF file.');
//     }
//   };

//   const handleUpload = async (e) => {
//     e.preventDefault();
//     const formData = new FormData();
//     formData.append('file', file);

//     try {
//       const token = localStorage.getItem('token');
//       const BASE_URL = `${window.location.protocol}//${window.location.hostname}`;
//       const response = await axios.post(`${BASE_URL}/resume/chat/`, formData, {
//         headers: {
//           'Content-Type': 'multipart/form-data',
//           'Authorization': `Token ${token}`,
//         },
//       });

//       setMessage('File uploaded successfully');
//       console.log('File uploaded:', response.data);
//       onUploadSuccess();

//     } catch (error) {
//       setMessage('Error uploading file');
//       console.error('Error uploading file:', error);
//     }
//   };

//   return (
//     <div className="upload-resume-container">
//       <h1 className="upload-resume-heading">Upload Resume</h1>
//       <form onSubmit={handleUpload} className="upload-form">
//         <input type="file" onChange={handleFileChange} className="file-input" />
//         <button type="submit" className="submit-button">Find Matching Jobs</button>
//       </form>
//       {message && <p className="message">{message}</p>}

//       {/* Display PDF Preview if a file is selected */}
//       {filePreview && (
//         <div className="pdf-preview-container">
//           <embed src={filePreview} width="400" height="400" type="application/pdf" className="pdf-preview" />
//         </div>
//       )}
//     </div>

//   );
// };

// export default ResumeUpload;



import React, { useState } from 'react';
import axios from 'axios';
import './ResumeUpload.css';

const ResumeUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [filePreview, setFilePreview] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);

      const reader = new FileReader();
      reader.onloadend = () => {
        setFilePreview(reader.result);
      };
      reader.readAsDataURL(selectedFile);
    } else {
      setMessage('Please select a valid PDF file.');
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('token');
      const BASE_URL = `${window.location.protocol}//${window.location.hostname}:8000`;
      const response = await axios.post(`${BASE_URL}/resume/chat/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Token ${token}`,
        },
      });

      setMessage('File uploaded successfully');
      console.log('File uploaded:', response.data);
      onUploadSuccess();
    } catch (error) {
      setMessage('Error uploading file');
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div className="upload-resume-container">
      {/* Display the uploaded file name in place of the heading */}
      <h1 className="upload-resume-heading">
        {file ? `Resume:` : 'Upload Resume'}
      </h1>

      <form onSubmit={handleUpload} className="upload-form">
        <input type="file" onChange={handleFileChange} className="file-input" />
        <button type="submit" className="submit-button">Find Matching Jobs</button>
      </form>

      {message && <p className="message">{message}</p>}

      {filePreview && (
        <div className="pdf-preview-container">
          <embed src={filePreview} width="400" height="400" type="application/pdf" className="pdf-preview" />
        </div>
      )}
    </div>
  );
};

export default ResumeUpload;
