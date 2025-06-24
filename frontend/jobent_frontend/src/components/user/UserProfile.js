import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './UserProfile.css';

const UserProfile = () => {
  const [userProfile, setUserProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          setError('You must be logged in to view your profile.');
          setLoading(false);
          return;
        }
        const BASE_URL = `${window.location.protocol}//${window.location.hostname}:8000`;
        const response = await axios.get(`${BASE_URL}/api/profile/`, {
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json',
          },
        });

        setUserProfile(response.data);
      } catch (error) {
        setError('Error fetching user profile.');
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!userProfile) {
    return <div className="no-profile">No profile found.</div>;
  }

  return (
    <div className="profile">
      <div className="profile-header">
        <div className="profile-details">
          <h1>{userProfile.first_name} {userProfile.last_name}</h1>
          <p>{userProfile.job_title}</p>
        </div>
      </div>
      <div className="profile-content">
        <p><strong>Email:</strong> {userProfile.email}</p>
        <p><strong>User Type:</strong> {userProfile.user_type}</p>
        <p><strong>Tokens:</strong> {userProfile.tokens}</p>
        <p><strong>Premium Status:</strong> {userProfile.is_premium ? 'premium' : 'normal'}</p>
      </div>
    </div>
  );
};

export default UserProfile;
