// import React, { useState, useEffect } from 'react';

// const RecentConversation = () => {
//     const [conversation, setConversation] = useState(null);

//     // Fetch the most recent conversation from the backend
//     useEffect(() => {
//         const fetchConversation = async () => {
//             try {
//                 const response = await fetch('http://localhost:8000/resume/chat/', { method: 'GET' });
//                 if (response.ok) {
//                     const data = await response.json();
//                     setConversation(data);
//                 } else {
//                     console.error('Failed to fetch conversation');
//                 }
//             } catch (error) {
//                 console.error('Error fetching conversation:', error);
//             }
//         };

//         fetchConversation();
//     }, []); // Empty dependency array to fetch only once when component mounts

//     return (
//         <div>
//             <h2>Recent Conversation</h2>
//             {conversation ? (
//                 <div>
//                     <p><strong>Question:</strong> {conversation.question}</p>
//                     <p><strong>Reply:</strong> {conversation.reply}</p>
//                 </div>
//             ) : (
//                 <p>Loading recent conversation...</p>
//             )}
//         </div>
//     );
// };
    
// export default RecentConversation;



import React, { useState, useEffect } from 'react';

const RecentConversation = () => {
    const [conversation, setConversation] = useState(null);

    // Function to get the CSRF token from cookies (same as before)
    const getCSRFToken = () => {
        const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
        return csrfToken ? csrfToken.split('=')[1] : '';
    };

    // Fetch the most recent conversation from the backend
    useEffect(() => {
        const fetchConversation = async () => {
            try {
                // Retrieve the token from localStorage
                const token = localStorage.getItem('token');
                if (!token) {
                    console.error('No token found in localStorage');
                    return; // Early exit if no token
                }

                console.log("Authorization Header:", `Token ${token}`); // Log the token for debugging

                // Send the request with the token in the Authorization header
                const response = await fetch('http://localhost:8000/resume/chat/', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Token ${token}`, // Include the token in the headers
                        'X-CSRFToken': getCSRFToken(),  // Include CSRF token if needed
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    setConversation(data);  // Set the conversation data
                } else {
                    console.error('Failed to fetch conversation');
                }
            } catch (error) {
                console.error('Error fetching conversation:', error);
            }
        };

        fetchConversation();
    }, []); // Empty dependency array to fetch only once when component mounts

    return (
        <div>
            <h2>Recent Conversation</h2>
            {conversation ? (
                <div>
                    <p><strong>Question:</strong> {conversation.question}</p>
                    <p><strong>Reply:</strong> {conversation.reply}</p>
                </div>
            ) : (
                <p>Loading recent conversation...</p>
            )}
        </div>
    );
};

export default RecentConversation;
