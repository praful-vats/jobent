// // src/api/resumeApi.js
// import axios from 'axios';

// // Update the base URL for upload
// const BASE_URL = "http://127.0.0.1:8000/";  // Removed the /api part

// // Function to upload a resume
// export const uploadResume = async (file) => {
//   const formData = new FormData();
//   formData.append("file", file);

//   try {
//     const response = await axios.post(`${BASE_URL}upload/`, formData, {
//       headers: { "Content-Type": "multipart/form-data" },
//     });
//     return response.data;  // Return the response data if successful
//   } catch (error) {
//     if (error.response) {
//       // The request was made and the server responded with a status other than 2xx
//       console.error("Error response data:", error.response.data);
//       console.error("Error response status:", error.response.status);
//       console.error("Error response headers:", error.response.headers);
//       throw new Error(`Upload failed: ${error.response.data.detail || 'Unknown error'}`);
//     } else if (error.request) {
//       // The request was made but no response was received
//       console.error("No response received:", error.request);
//       throw new Error("No response received from the server.");
//     } else {
//       // Something happened in setting up the request
//       console.error("Error message:", error.message);
//       throw new Error(`Error: ${error.message}`);
//     }
//   }
// };

// // Function to rewrite a resume
// export const rewriteResume = async (resumeId, jobDescription) => {
//   try {
//     const response = await axios.put(`${BASE_URL}rewrite/${resumeId}/`, { job_description: jobDescription });
    
//     // Ensure response contains 'rewritten_resume'
//     if (response.data && response.data.rewritten_resume) {
//       return response.data;  // Return the rewritten resume if available
//     } else {
//       throw new Error('No rewritten resume found in the response.');
//     }
//   } catch (error) {
//     if (error.response) {
//       // Handle error response
//       console.error("Error response data:", error.response.data);
//       console.error("Error response status:", error.response.status);
//       console.error("Error response headers:", error.response.headers);
//       throw new Error(`Rewrite failed: ${error.response.data.detail || 'Unknown error'}`);
//     } else if (error.request) {
//       // No response received
//       console.error("No response received:", error.request);
//       throw new Error("No response received from the server.");
//     } else {
//       // Error in setting up the request
//       console.error("Error message:", error.message);
//       throw new Error(`Error: ${error.message}`);
//     }
//   }
// };





// src/api/resumeApi.js
import axios from 'axios';

// Update the base URL for upload
const BASE_URL = "http://127.0.0.1:8000/";  // Removed the /api part

// Function to upload a resume
export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(`${BASE_URL}upload/`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;  // Return the response data if successful
  } catch (error) {
    if (error.response) {
      // The request was made and the server responded with a status other than 2xx
      console.error("Error response data:", error.response.data);
      console.error("Error response status:", error.response.status);
      console.error("Error response headers:", error.response.headers);
      throw new Error(`Upload failed: ${error.response.data.detail || 'Unknown error'}`);
    } else if (error.request) {
      // The request was made but no response was received
      console.error("No response received:", error.request);
      throw new Error("No response received from the server.");
    } else {
      // Something happened in setting up the request
      console.error("Error message:", error.message);
      throw new Error(`Error: ${error.message}`);
    }
  }
};

// Function to rewrite a resume
export const rewriteResume = async (resumeId, jobDescription) => {
    try {
      const response = await axios.put(`${BASE_URL}rewrite/${resumeId}/`, { job_description: jobDescription }, {
        responseType: 'arraybuffer', // Ensure we get the binary data (PDF)
      });
  
      // Check if the response is a PDF (it will have a content-type of 'application/pdf')
      if (response.headers['content-type'] === 'application/pdf') {
        return response; // Return the full response, including the PDF data
      } else {
        // In case it's not a PDF, check if there is a rewritten resume in the response
        if (response.data && response.data.rewritten_resume) {
          return response.data;  // Return the rewritten resume text if available
        } else {
          throw new Error("No rewritten resume found in the response.");
        }
      }
    } catch (error) {
      if (error.response) {
        console.error("Error response data:", error.response.data);
        console.error("Error response status:", error.response.status);
        throw new Error(`Rewrite failed: ${error.response.data.detail || 'Unknown error'}`);
      } else if (error.request) {
        console.error("No response received:", error.request);
        throw new Error("No response received from the server.");
      } else {
        console.error("Error message:", error.message);
        throw new Error(`Error: ${error.message}`);
      }
    }
  };
  