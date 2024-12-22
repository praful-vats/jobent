from groq import Groq  # type: ignore
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)
MAX_TOKENS = 30000

def truncate_text(text, max_length=3000):
    """
    Truncate the text to a specified maximum length to fit the token limit.
    """
    return text[:max_length]

def rewrite_resume(original_resume, job_description):
    # Prepare the structured input for Groq API
    structured_resume = f"""
    Summary:
    {original_resume['summary']}
    
    Skills:
    {original_resume['skills']}
    
    Experience:
    {original_resume['experience']}
    
    Education:
    {original_resume['education']}
    
    Projects:
    {original_resume['projects']}
    """
    
    # Truncate resume if it exceeds the max length
    truncated_resume = truncate_text(structured_resume, max_length=3000)
    truncated_prompt = f"""
    Rewrite the following resume to fit the provided job description. Focus solely on the resume content, ensuring it aligns with the job description. 
    Do not add any company names, explanatory notes, or comments.
    Resume:
    {truncated_resume}
    Job Description:
    {job_description}
    """
    
    # Log token count to ensure it fits within limits
    token_count = len(truncated_prompt.split())
    print(f"Token count: {token_count} (Max: {MAX_TOKENS})")

    if token_count > MAX_TOKENS:
        return "The input exceeds the token limit. Please shorten the resume or job description."

    try:
        # Request Groq API to rewrite the resume
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",  # Use the model you're working with
            messages=[ 
                {"role": "user", "content": truncated_prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            stream=False
        )

        # Log the full response for debugging
        print("Groq API Full Response:", chat_completion)  

        # Extract the rewritten resume from the response
        rewritten_resume = chat_completion.choices[0].message.content.strip()

        # Return only the rewritten resume (exclude change notes or unnecessary parts)
        return rewritten_resume

    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return f"An error occurred while rewriting the resume: {str(e)}"
    

def generate_cover_letter(rewritten_resume, job_description):
    """
    Generate a custom cover letter based on the rewritten resume and job description.
    """
    prompt = f"""
    Create a professional cover letter based on the following rewritten resume and job description:
    
    Rewritten Resume:
    {rewritten_resume}
    
    Job Description:
    {job_description}
    """

    try:
        # Request Groq API to generate the cover letter
        chat_completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            stream=False
        )

        # Extract the cover letter from the response
        cover_letter = chat_completion.choices[0].message.content.strip()
        return cover_letter

    except Exception as e:
        print(f"Error calling Groq API for cover letter: {e}")
        return f"An error occurred while generating the cover letter: {str(e)}"
