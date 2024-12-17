import React, { useState } from 'react';
import axios from 'axios';

const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('token');
      console.log("Token:", token);

      const response = await axios.post('http://localhost:8000/resume/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Token ${token}`,
        },
      });
      setMessage('File uploaded successfully');
      console.log('File uploaded:', response.data);
    } catch (error) {
      setMessage('Error uploading file');
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div>
      <h1>Upload Resume</h1>
      <form onSubmit={handleUpload}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default ResumeUpload;