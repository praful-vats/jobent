// import React, { useState } from 'react';
// import axios from 'axios';
// import { useNavigate } from 'react-router-dom';

// const SignupPage = () => {
//   const [email, setEmail] = useState('');
//   const [password, setPassword] = useState('');
//   const [error, setError] = useState('');
//   const navigate = useNavigate();

//   const handleSignup = async (e) => {
//     e.preventDefault();
//     try {
//       const response = await axios.post('http://localhost:8000/api/signup/', {
//         username: email,
//         password: password,
//       });
//       localStorage.setItem('token', response.data.token);
//       navigate('/service');
//     } catch (err) {
//       setError('Username already exists');
//     }
//   };

//   return (
//     <div>
//       <h1>Signup</h1>
//       <form onSubmit={handleSignup}>
//         <div>
//           <label>Email:</label>
//           <input
//             type="email"
//             name="email"
//             value={email}
//             onChange={(e) => setEmail(e.target.value)}
//             required
//           />
//         </div>
//         <div>
//           <label>Password:</label>
//           <input
//             type="password"
//             name="password"
//             value={password}
//             onChange={(e) => setPassword(e.target.value)}
//             required
//           />
//         </div>
//         {error && <p>{error}</p>}
//         <button type="submit">Signup</button>
//       </form>
//     </div>
//   );
// };

// export default SignupPage;



import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './SignupPage.css';

const SignupPage = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    birthday: '',
    gender: '',
    username: '',
    password: '',
    confirmPassword: '',
    agreeToTerms: false
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    try {
      const response = await axios.post('http://localhost:8000/api/signup/', {
        email: formData.email,
        password: formData.password,
        firstName: formData.firstName,
        lastName: formData.lastName,
        birthday: formData.birthday,
      });
      localStorage.setItem('token', response.data.token);
      navigate('/service');
    } catch (err) {
      setError('Signup failed');
    }
  };
  

  return (
    <div className='con'>
      <h1 className="signup-title">SIGN UP</h1>
      <div className="signup-container">
      <form onSubmit={handleSignup} className="signup-form">
          <div className="name-group">
          <input
              type="text"
              name="firstName"
              placeholder="FIRST NAME"
              value={formData.firstName}
              onChange={handleChange}
              // required
          />
          <input
              type="text"
              name="lastName"
              placeholder="LAST NAME"
              value={formData.lastName}
              onChange={handleChange}
              // required
          />
          </div>
          
          <input
          type="email"
          name="email"
          placeholder="EMAIL ADDRESS"
          value={formData.email}
          onChange={handleChange}
          required
          />
          
          <div className="birth-gender-group">
          <input
              type="date"
              name="birthday"
              placeholder="BIRTHDAY"
              value={formData.birthday}
              onChange={handleChange}
              // required
          />
          
          </div>
          
          <input
          type="password"
          name="password"
          placeholder="PASSWORD"
          value={formData.password}
          onChange={handleChange}
          required
          />
          
          <input
          type="password"
          name="confirmPassword"
          placeholder="CONFIRM PASSWORD"
          value={formData.confirmPassword}
          onChange={handleChange}
          // required
          />

          

          {error && <p className="error-message">{error}</p>}
          
          <button type="submit" className="continue-button">CONTINUE</button>
      </form>
      </div>
    </div>
  );
};

export default SignupPage;
