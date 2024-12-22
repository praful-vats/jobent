# from groq import Groq  # type: ignore

# # Initialize Groq client with the provided API key
# GROQ_API_KEY = "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"
# client = Groq(api_key=GROQ_API_KEY)

# def generate_reply(input_text):
#     # Check for scheduling or follow-up context
#     if "schedule" in input_text.lower() or "available" in input_text.lower() or "google meet" in input_text.lower() or "calendly" in input_text.lower():
#         prompt = f"HR is asking about interview availability or scheduling. Provide a professional reply regarding scheduling an interview or confirming availability. Input: {input_text}\n"
#     elif "follow up" in input_text.lower() or "reminder" in input_text.lower():
#         prompt = f"HR is following up on an already scheduled interview. Provide a polite follow-up message acknowledging the interview and checking for any additional updates or details. Input: {input_text}\n"
#     elif "failure" in input_text.lower() or "strengths" in input_text.lower() or "superhero" in input_text.lower():
#         # Out-of-the-box or behavioral questions
#         prompt = f"HR has asked an unconventional or behavioral question. Provide a thoughtful, professional, and reflective response to the following question: {input_text}\n"
#     else:
#         # Standard candidate reply for typical job-related queries
#         prompt = f"Provide a professional response as a candidate to the following HR question: {input_text}\n"
    
#     try:
#         # Send the input text as a 'user' message to Groq API
#         chat_completion = client.chat.completions.create(
#             model="llama3-8b-8192",  # Use the model you're working with
#             messages=[
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.7,
#             max_tokens=150,
#             top_p=1,
#             stream=False
#         )

#         # Extract the response text
#         reply = chat_completion.choices[0].message.content.strip()

#         return reply

#     except Exception as e:
#         print(f"Error: {e}")
#         return f"I'm sorry, I couldn't generate a response at the moment. Error: {str(e)}"

# def process_conversation(input_text):
#     # Handle different types of conversations internally based on the content
#     return generate_reply(input_text)





# from groq import Groq  # type: ignore

# # Initialize Groq client with the provided API key
# GROQ_API_KEY = "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"
# client = Groq(api_key=GROQ_API_KEY)

# def generate_reply(input_text):
#     # Check for scheduling or follow-up context
#     if "schedule" in input_text.lower() or "available" in input_text.lower() or "google meet" in input_text.lower() or "calendly" in input_text.lower():
#         prompt = f"HR is asking about interview availability or scheduling. Provide a professional reply regarding scheduling an interview or confirming availability. Input: {input_text}\n"
#     elif "follow up" in input_text.lower() or "reminder" in input_text.lower():
#         prompt = f"HR is following up on an already scheduled interview. Provide a polite follow-up message acknowledging the interview and checking for any additional updates or details. Input: {input_text}\n"
#     elif "failure" in input_text.lower() or "strengths" in input_text.lower() or "superhero" in input_text.lower():
#         # Out-of-the-box or behavioral questions
#         prompt = f"HR has asked an unconventional or behavioral question. Provide a thoughtful, professional, and reflective response to the following question: {input_text}\n"
#     else:
#         # Standard candidate reply for typical job-related queries
#         prompt = f"Provide a professional response as a candidate to the following HR question: {input_text}\n"
    
#     try:
#         # Send the input text as a 'user' message to Groq API
#         chat_completion = client.chat.completions.create(
#             model="llama3-8b-8192",  # Use the model you're working with
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.7,
#             max_tokens=150,
#             top_p=1,
#             stream=False
#         )

#         # Extract the response text
#         reply = chat_completion.choices[0].message.content.strip()

#         # If the input mentions scheduling, ask for the date and time
#         if "schedule" in input_text.lower():
#             reply += "\n\nPlease provide your available time slots for the interview."

#         return reply

#     except Exception as e:
#         print(f"Error: {e}")
#         return f"I'm sorry, I couldn't generate a response at the moment. Error: {str(e)}"

# def process_conversation(input_text):
#     # Handle different types of conversations internally based on the content
#     return generate_reply(input_text)



#example1
# from groq import Groq  # type: ignore

# # Initialize Groq client with the provided API key
# GROQ_API_KEY = "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"
# client = Groq(api_key=GROQ_API_KEY)

# # Store conversation history to improve responses
# conversation_history = []

# def generate_reply(input_text):
#     """Generate a professional reply based on input text."""
#     global conversation_history

#     # Check for scheduling or follow-up context
#     if any(keyword in input_text.lower() for keyword in ["schedule", "available", "google meet", "calendly"]):
#         prompt = (
#             "HR is asking about interview availability or scheduling. "
#             "Provide a professional reply regarding scheduling an interview or confirming availability."
#             f"\nInput: {input_text}"
#         )
#     elif any(keyword in input_text.lower() for keyword in ["follow up", "reminder"]):
#         prompt = (
#             "HR is following up on an already scheduled interview. "
#             "Provide a polite follow-up message acknowledging the interview and checking for any additional updates or details."
#             f"\nInput: {input_text}"
#         )
#     elif any(keyword in input_text.lower() for keyword in ["failure", "strengths", "superhero"]):
#         prompt = (
#             "HR has asked an unconventional or behavioral question. "
#             "Provide a thoughtful, professional, and reflective response."
#             f"\nInput: {input_text}"
#         )
#     else:
#         prompt = (
#             "Provide a professional response as a candidate to the following HR question."
#             f"\nInput: {input_text}"
#         )

#     try:
#         # Send the input text as a 'user' message to Groq API
#         chat_completion = client.chat.completions.create(
#             model="llama3-8b-8192",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.7,
#             max_tokens=150,
#             top_p=1,
#             stream=False
#         )

#         # Extract the response text
#         reply = chat_completion.choices[0].message.content.strip()

#         # Add clarifying request if scheduling is mentioned
#         if "schedule" in input_text.lower():
#             reply += "\n\nPlease provide your available time slots for the interview."

#         # Save input and reply for learning context
#         conversation_history.append({"question": input_text, "reply": reply})

#         return reply

#     except Exception as e:
#         return f"I'm sorry, I couldn't generate a response at the moment. Error: {str(e)}"

# def process_conversation(input_text):
#     """Process the input text and generate appropriate responses."""
#     return generate_reply(input_text)

# # Example usage
# if __name__ == "__main__":
#     while True:
#         user_input = input("HR Question or Statement: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("Ending the conversation.")
#             break
#         reply = process_conversation(user_input)
#         print(f"Candidate Reply: {reply}")

#example2:
# from groq import Groq  # type: ignore

# # Initialize Groq client with the provided API key
# GROQ_API_KEY = "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"
# client = Groq(api_key=GROQ_API_KEY)

# # Store conversation history to improve responses
# conversation_history = []

# def generate_reply(input_text):
#     """Generate a professional and intelligent reply based on input text."""
#     global conversation_history

#     # Identify the type of input context
#     input_lower = input_text.lower()
#     if any(keyword in input_lower for keyword in ["schedule", "available", "google meet", "calendly"]):
#         prompt = (
#             "HR is asking about interview availability or scheduling. "
#             "Provide a professional reply regarding scheduling an interview or confirming availability."
#             f"\nInput: {input_text}"
#         )
#     elif any(keyword in input_lower for keyword in ["follow up", "reminder"]):
#         prompt = (
#             "HR is following up on an already scheduled interview. "
#             "Provide a polite follow-up message acknowledging the interview and checking for any additional updates or details."
#             f"\nInput: {input_text}"
#         )
#     elif any(keyword in input_lower for keyword in ["failure", "strengths", "superhero", "challenge", "weakness"]):
#         prompt = (
#             "HR has asked an unconventional or behavioral question. "
#             "Provide a thoughtful, professional, and reflective response."
#             f"\nInput: {input_text}"
#         )
#     elif "why" in input_lower or "reason" in input_lower:
#         prompt = (
#             "HR is asking a reason-based or motivational question. "
#             "Craft a compelling and professional response that highlights the candidate's strengths and alignment with the role."
#             f"\nInput: {input_text}"
#         )
#     else:
#         prompt = (
#             "Provide a professional response as a candidate to the following HR question."
#             f"\nInput: {input_text}"
#         )

#     try:
#         # Send the input text as a 'user' message to Groq API
#         chat_completion = client.chat.completions.create(
#             model="llama3-8b-8192",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.7,
#             max_tokens=200,
#             top_p=1,
#             stream=False
#         )

#         # Extract the response text
#         reply = chat_completion.choices[0].message.content.strip()

#         # Add clarifying request if scheduling is mentioned
#         if "schedule" in input_lower:
#             reply += "\n\nPlease provide your available time slots for the interview."

#         # Save input and reply for learning context
#         conversation_history.append({"question": input_text, "reply": reply})

#         return reply

#     except Exception as e:
#         return f"I'm sorry, I couldn't generate a response at the moment. Error: {str(e)}"

# def process_conversation(input_text):
#     """Process the input text and generate appropriate responses."""
#     global conversation_history

#     # Check for continuity and adapt responses
#     if conversation_history:
#         last_entry = conversation_history[-1]
#         if last_entry["question"] in input_text:
#             input_text += f"\nContext: {last_entry['reply']}"

#     return generate_reply(input_text)

# # Example usage
# if __name__ == "__main__":
#     print("Candidate Bot Initialized. Type 'exit' or 'quit' to end.")
#     while True:
#         user_input = input("HR Question or Statement: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("Ending the conversation.")
#             break
#         reply = process_conversation(user_input)
#         print(f"Candidate Reply: {reply}")


#works
# from groq import Groq  # type: ignore

# # Initialize Groq client with the provided API key
# GROQ_API_KEY = "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"
# client = Groq(api_key=GROQ_API_KEY)

# # Store conversation history to improve responses
# conversation_history = []

# def generate_reply(input_text):
#     """Generate a professional and intelligent reply based on input text."""
#     global conversation_history

#     # Identify the type of input context
#     input_lower = input_text.lower()
#     if any(keyword in input_lower for keyword in ["schedule", "available", "google meet", "calendly"]):
#         prompt = (
#             "HR is asking about interview availability or scheduling. "
#             "Provide a professional reply regarding scheduling an interview or confirming availability."
#             f"\nInput: {input_text}"
#         )
#     elif any(keyword in input_lower for keyword in ["follow up", "reminder"]):
#         prompt = (
#             "HR is following up on an already scheduled interview. "
#             "Provide a polite follow-up message acknowledging the interview and checking for any additional updates or details."
#             f"\nInput: {input_text}"
#         )
#     elif any(keyword in input_lower for keyword in ["failure", "strengths", "superhero", "challenge", "weakness"]):
#         prompt = (
#             "HR has asked an unconventional or behavioral question. "
#             "Provide a thoughtful, professional, and reflective response."
#             f"\nInput: {input_text}"
#         )
#     elif "why" in input_lower or "reason" in input_lower:
#         prompt = (
#             "HR is asking a reason-based or motivational question. "
#             "Craft a compelling and professional response that highlights the candidate's strengths and alignment with the role."
#             f"\nInput: {input_text}"
#         )
#     else:
#         prompt = (
#             "Provide a professional response as a candidate to the following HR question."
#             f"\nInput: {input_text}"
#         )

#     try:
#         # Send the input text as a 'user' message to Groq API
#         chat_completion = client.chat.completions.create(
#             model="llama3-8b-8192",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.7,
#             max_tokens=200,
#             top_p=1,
#             stream=False
#         )

#         # Extract the response text
#         reply = chat_completion.choices[0].message.content.strip()

#         # Add clarifying request if scheduling is mentioned
#         if any(keyword in input_lower for keyword in ["schedule", "calendly", "available"]):
#             reply += "\n\nPlease provide your available time slots for the interview using the scheduling link."

#         # Save input and reply for learning context
#         conversation_history.append({"question": input_text, "reply": reply})

#         return reply

#     except Exception as e:
#         return f"I'm sorry, I couldn't generate a response at the moment. Error: {str(e)}"

# def process_conversation(input_text):
#     """Process the input text and generate appropriate responses."""
#     global conversation_history

#     # Check for continuity and adapt responses
#     if conversation_history:
#         last_entry = conversation_history[-1]
#         if last_entry["question"] in input_text:
#             input_text += f"\nContext: {last_entry['reply']}"

#     return generate_reply(input_text)



from groq import Groq  # type: ignore

# Initialize Groq client with the provided API key
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

def generate_reply(input_text):
    """Generate a professional and intelligent reply based on input text."""
    input_lower = input_text.lower()

    # Identify the type of input context
    if any(keyword in input_lower for keyword in ["schedule", "available", "google meet", "calendly"]):
        prompt = (
            "HR is asking about interview availability or scheduling. "
            "Provide a professional reply regarding scheduling an interview or confirming availability."
            f"\nInput: {input_text}"
        )
    elif any(keyword in input_lower for keyword in ["follow up", "reminder"]):
        prompt = (
            "HR is following up on an already scheduled interview. "
            "Provide a polite follow-up message acknowledging the interview and checking for any additional updates or details."
            f"\nInput: {input_text}"
        )
    elif any(keyword in input_lower for keyword in ["failure", "strengths", "superhero", "challenge", "weakness"]):
        prompt = (
            "HR has asked an unconventional or behavioral question. "
            "Provide a thoughtful, professional, and reflective response."
            f"\nInput: {input_text}"
        )
    elif "why" in input_lower or "reason" in input_lower:
        prompt = (
            "HR is asking a reason-based or motivational question. "
            "Craft a compelling and professional response that highlights the candidate's strengths and alignment with the role."
            f"\nInput: {input_text}"
        )
    else:
        prompt = (
            "Provide a professional response as a candidate to the following HR question."
            f"\nInput: {input_text}"
        )

    try:
        # Send the input text as a 'user' message to Groq API
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=200,
            top_p=1,
            stream=False
        )

        # Extract the response text
        reply = chat_completion.choices[0].message.content.strip()

        return reply

    except Exception as e:
        return f"I'm sorry, I couldn't generate a response at the moment. Error: {str(e)}"

def process_conversation(input_text, user_id, conversation_history):
    """Process the input text and generate appropriate responses, storing conversation history."""
    # Check continuity and adapt responses
    if conversation_history.exists():  # Ensures history is not empty
        last_entry = conversation_history.last()  # Get the most recent conversation
        input_text += f"\nPrevious reply: {last_entry.reply}"
        
    return generate_reply(input_text)
