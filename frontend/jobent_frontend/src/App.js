import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LandingPage from "./components/landing/LandingPage";
import LoginPage from "./components/landing/LoginPage";
import SignupPage from "./components/landing/SignupPage";
import ResumeUpload from "./components/resume/ResumeUpload";
import ResumeList from "./components/resume/ResumeList";
import ServicePage from "./components/service/ServicePage";
import JobSearch from "./components/job_search/JobSearch";
import UserProfile from "./components/user/UserProfile"; 
import Premium from "./components/premium/Premium";

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/service" element={<ServicePage />} />
        <Route path="/service/resume/upload" element={<ResumeUpload />} />
        <Route path="/service/resume/list" element={<ResumeList />} />
        <Route path="/service/job/search" element={<JobSearch />} />
        <Route path="/profile" element={<UserProfile />} />
        <Route path="/premium" element={<Premium />} />
        {/* Add other routes here */}
      </Routes>
    </Router>
  );
}

export default App;