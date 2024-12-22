// import React, { useState } from 'react';
// import './Chatbot.css';

// // Function to get the CSRF token from cookies
// const getCSRFToken = () => {
//     const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
//     return csrfToken ? csrfToken.split('=')[1] : '';
// };

// const Chatbot = () => {
//     const [userInput, setUserInput] = useState('');
//     const [chatHistory, setChatHistory] = useState([]);

//     // Function to handle user input and fetch response from Django backend
//     const handleSubmit = async (e) => {
//         e.preventDefault();

//         if (userInput.trim()) {
//             // Add user input to chat history
//             setChatHistory((prevHistory) => [
//                 ...prevHistory,
//                 { sender: 'user', text: userInput },
//             ]);

//             try {
//                 // Send the user input to the Django backend
//                 const response = await fetch('http://localhost:8000/resume/chat/', {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json',
//                         'X-CSRFToken': getCSRFToken(),  // Include CSRF token
//                     },
//                     body: JSON.stringify({ user_input: userInput }),  // Send user input as JSON
//                 });

//                 const data = await response.json();

//                 // Add bot response to chat history
//                 setChatHistory((prevHistory) => [
//                     ...prevHistory,
//                     { sender: 'bot', text: data.reply },
//                 ]);

//                 // Clear user input field
//                 setUserInput('');
//             } catch (error) {
//                 console.error('Error sending message:', error);
//                 setChatHistory((prevHistory) => [
//                     ...prevHistory,
//                     { sender: 'bot', text: "I'm sorry, I couldn't process your request." },
//                 ]);
//             }
//         }
//     };

//     return (
//         <div className="chat-container">
//             <div className="chat-history">
//                 {chatHistory.map((message, index) => (
//                     <div
//                         key={index}
//                         className={message.sender === 'user' ? 'user-message' : 'bot-message'}
//                     >
//                         <p>{message.text}</p>
//                     </div>
//                 ))}
//             </div>

//             <form onSubmit={handleSubmit} className="chat-form">
//                 <input
//                     type="text"
//                     value={userInput}
//                     onChange={(e) => setUserInput(e.target.value)}
//                     placeholder="Enter your question..."
//                     required
//                 />
//                 <button type="submit">Send</button>
//             </form>
//         </div>
//     );
// };

// export default Chatbot;






import React, { useState } from 'react';
import './Chatbot.css';

// Function to get the CSRF token from cookies
const getCSRFToken = () => {
    const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return csrfToken ? csrfToken.split('=')[1] : '';
};

const Chatbot = () => {
    const [userInput, setUserInput] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const [isScheduling, setIsScheduling] = useState(false);
    const [scheduleDetails, setScheduleDetails] = useState('');

    // Function to handle user input and fetch response from Django backend
    const handleSubmit = async (e) => {
        e.preventDefault();

        if (userInput.trim()) {
            // Add user input to chat history
            setChatHistory((prevHistory) => [
                ...prevHistory,
                { sender: 'user', text: userInput },
            ]);

            try {
                // Send the user input to the Django backend
                const token = localStorage.getItem('token');
                console.log("Token:", token);

                if (!token) {
                    console.log("No token found in localStorage");
                    return; // Optionally handle the missing token case
                }
                
                const response = await fetch('http://localhost:8000/resume/chat/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${token}`,
                        'X-CSRFToken': getCSRFToken(),  // Include CSRF token
                    },
                    body: JSON.stringify({ user_input: userInput }),  // Send user input as JSON
                });

                const data = await response.json();

                if (data.reply.toLowerCase().includes('schedule')) {
                    // If the bot mentions scheduling, set the state to handle scheduling
                    setIsScheduling(true);
                    setScheduleDetails('Please provide your available time slots.');
                } else {
                    // Add bot response to chat history
                    setChatHistory((prevHistory) => [
                        ...prevHistory,
                        { sender: 'bot', text: data.reply },
                    ]);
                }

                // Clear user input field
                setUserInput('');
            } catch (error) {
                console.error('Error sending message:', error);
                setChatHistory((prevHistory) => [
                    ...prevHistory,
                    { sender: 'bot', text: "I'm sorry, I couldn't process your request." },
                ]);
            }
        }
    };

    // Function to handle scheduling input
    const handleScheduling = async () => {
        if (scheduleDetails.trim()) {
            try {
                const token = localStorage.getItem('token');
                console.log("Token:", token);
                const response = await fetch('http://localhost:8000/resume/chat/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Token ${token}`,
                        'X-CSRFToken': getCSRFToken(),
                    },
                    body: JSON.stringify({ user_input: userInput }),
                });

                const data = await response.json();

                // Handle bot's response after scheduling
                setChatHistory((prevHistory) => [
                    ...prevHistory,
                    { sender: 'bot', text: data.reply || 'Interview successfully scheduled.' },
                ]);

                setIsScheduling(false);
                setScheduleDetails('');
            } catch (error) {
                console.error('Error scheduling interview:', error);
                setChatHistory((prevHistory) => [
                    ...prevHistory,
                    { sender: 'bot', text: "Sorry, I couldn't schedule the interview." },
                ]);
            }
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-history">
                {chatHistory.map((message, index) => (
                    <div
                        key={index}
                        className={message.sender === 'user' ? 'user-message' : 'bot-message'}
                    >
                        <p>{message.text}</p>
                    </div>
                ))}
            </div>

            <form onSubmit={handleSubmit} className="chat-form">
                <input
                    type="text"
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    placeholder="Enter your question..."
                    required
                />
                <button type="submit">Send</button>
            </form>

            {isScheduling && (
                <div className="schedule-form">
                    <textarea
                        value={scheduleDetails}
                        onChange={(e) => setScheduleDetails(e.target.value)}
                        placeholder="Enter your availability..."
                        rows="4"
                    />
                    <button onClick={handleScheduling}>Schedule Interview</button>
                </div>
            )}
        </div>
    );
};

export default Chatbot;
