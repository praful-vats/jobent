import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LandingPage from "./components/landing/LandingPage";
import LoginPage from "./components/landing/LoginPage";
import SignupPage from "./components/landing/SignupPage";
import ResumeUpload from "./components/resume/ResumeUpload";
import ResumeList from "./components/resume/ResumeList";
import ServicePage from "./components/service/ServicePage";
import JobSearch from "./components/job_search/JobSearch";

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
        {/* Add other routes here */}
      </Routes>
    </Router>
  );
}

export default App;