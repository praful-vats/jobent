from groq import Groq

# Initialize the Groq client and pass the API key
GROQ_API_KEY = "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"  # Ensure your actual API key is used
client = Groq(api_key=GROQ_API_KEY)

# Max tokens for Groq's model
MAX_TOKENS = 30000  # This is the limit for the model you're using

def truncate_text(text, max_length=3000):
    """
    Truncate the text to a specified maximum length to fit the token limit.
    """
    return text[:max_length]

# groq_api.py
def rewrite_resume(original_resume, job_description):
    prompt = f"Rewrite this resume to match the following job description:\n{job_description}\n\nResume:\n{original_resume}"

    truncated_resume = truncate_text(original_resume, max_length=3000)
    truncated_prompt = f"Rewrite this resume to match the following job description:\n{job_description}\n\nResume:\n{truncated_resume}"

    try:
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[ 
                {"role": "system", "content": "You are a professional resume editor."},
                {"role": "user", "content": truncated_prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            stream=False
        )

        print("Groq API Full Response:", chat_completion)  # Log the full response for debugging

        # Extract the rewritten resume
        rewritten_resume = chat_completion.choices[0].message.content.strip()

        return rewritten_resume

    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return f"An error occurred while rewriting the resume: {str(e)}"
