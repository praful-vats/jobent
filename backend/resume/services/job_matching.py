from sentence_transformers import SentenceTransformer

# Initialize Hugging Face model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to truncate text if it's too long
def truncate_text(text, max_length=3000):
    return text[:max_length]

def rewrite_resume(original_resume, job_description):
    """
    Rewrites the resume according to the provided job description.
    """
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

    truncated_resume = truncate_text(structured_resume, max_length=3000)
    rewritten_resume = f"""
    Rewrite the following resume to fit the provided job description. Focus solely on the resume content, ensuring it aligns with the job description.
    Resume:
    {truncated_resume}
    Job Description:
    {job_description}
    """
    return rewritten_resume

def embed_text_with_model(text):
    """
    Generates embeddings for the resume using a Hugging Face model.
    """
    if not isinstance(text, str) or not text.strip():  # Ensure it's a valid non-empty string
        print(f"Error: Invalid text input. Received: {text}")
        return None

    try:
        embedding = model.encode(text).tolist()  # Hugging Face encoding
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None
