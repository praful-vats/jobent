import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './LoginPage.css';

const LoginPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/login/', {
        email: formData.email, // Fix: Use 'email' instead of 'username'
        password: formData.password,
      });
      localStorage.setItem('token', response.data.token);
      navigate('/service');
    } catch (err) {
      setError('Invalid credentials');
    }
  };
  

  return (
    <div className='con'>
      <h1 className="signup-title">LOGIN</h1>
      <div className="signup-container">
        <form onSubmit={handleLogin} className="signup-form">
          <input
            type="email"
            name="email"
            placeholder="EMAIL ADDRESS"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="PASSWORD"
            value={formData.password}
            onChange={handleChange}
            required
          />
          {error && <p className="error-message">{error}</p>}
          <button type="submit" className="continue-button">CONTINUE</button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
