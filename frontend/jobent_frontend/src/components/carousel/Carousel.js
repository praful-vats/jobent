import React from "react";
import "./Carousel.css";

const Carousel = () => {
  const jobs = [
    {
      title: "Software Engineer",
      skills: "Machine Learning, Deep Learning, Python",
      location: "Bangalore",
      company: "Google",
      score: 4.5,
      link: "https://example.com/software-engineer",
    },
    {
      title: "Frontend Intern",
      skills: "React, Next.js, TypeScript, CSS",
      location: "Hyderabad",
      company: "Microsoft",
      score: 4.0,
      link: "https://example.com/cloud-engineer",
    },
    {
      title: "Data Analyst",
      skills: "Data Analysis, Data Visualization, SQL",
      location: "Mumbai",
      company: "Amazon",
      score: 0,
      link: "https://example.com/hr-manager",
    },
    {
      title: "DevOps Engineer",
      skills: "DevOps, CI/CD, Cloud, Kubernetes",
      location: "Pune",
      company: "Facebook",
      score: 4.4,
      link: "https://example.com/intern",
    },
  ];

  // Duplicate the list to create a smooth infinite loop
  const repeatedJobs = [...jobs, ...jobs];

  return (
    <div className="carousel-container">
      <div className="vertical-scroll-container">
        {repeatedJobs.map((job, index) => (
          <div key={index} className="job-card">
            <a
              href={job.link}
              target="_blank"
              rel="noopener noreferrer"
              className="job-link"
            >
              {/* <p className="job" title={`𓁉`}>𓀦</p> */}
              <p className="job-title" title={`Job Title`}>{job.title}</p>
              <p className="job-skills" title={`Skills`}>{job.skills}</p>
              <p className="job-company" title={`Company`}>{job.company}</p>
              <p className="job-location" title={`Location`}>{job.location}</p>
              <p className="job-score" title={`Match Score / 5`}>{job.score}</p>

            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Carousel;
