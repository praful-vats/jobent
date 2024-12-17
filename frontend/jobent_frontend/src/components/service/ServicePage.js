import React from 'react';
import { Link } from 'react-router-dom';

const ServicePage = () => {
  return (
    <div>
      <h1>Service Options</h1>
      <ul>
        <li><Link to="/service/resume/upload">Upload Resume</Link></li>
        <li><Link to="/service/resume/list">List Resumes</Link></li>
        <li><Link to="/service/users">User Management</Link></li>
        <li><Link to="/service/job/search">Job Search</Link></li>
      </ul>
    </div>
  );
};

export default ServicePage;