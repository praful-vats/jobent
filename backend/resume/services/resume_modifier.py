import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# Initialize Pinecone
pc = Pinecone(api_key='pcsk_DigCf_K19DeFaAr4MxYpebqg6qd2YjkvT3GJidqYmXL7QgVT5f7L2V6cjd846Ykhs3F92')
index_name = "job3"

# Check if the index exists
if index_name not in pc.list_indexes().names():
    print(f"Error: Index {index_name} does not exist. Please create it in the Pinecone dashboard.")
else:
    index = pc.Index(index_name)

# Initialize Hugging Face SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')  # You can choose other models like 'distilbert-base-nli-stsb-mean-tokens'

# Function to truncate text to a max length
def truncate_text(text, max_length=3000):
    return text[:max_length]

# Function to rewrite the resume (no Groq API, just a placeholder)
def rewrite_resume(original_resume, job_description):
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
    truncated_prompt = f"""
    Rewrite the following resume to fit the provided job description. Focus solely on the resume content, ensuring it aligns with the job description.
    Resume:
    {truncated_resume}
    Job Description:
    {job_description}
    """
    # Here, you can run this through any LLM or just return the structured resume (no Groq call).
    return truncated_prompt

# Function to embed text using Hugging Face model
def embed_text_with_pinecone(text):
    if not isinstance(text, str) or not text.strip():  # Ensure it's a valid non-empty string
        print(f"Error: Invalid text input. Received: {text}")
        return None

    try:
        embedding = model.encode(text).tolist()  # Hugging Face encoding
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None


# Function to match jobs using Pinecone
def match_jobs(resume_content):
    resume_embedding = embed_text_with_pinecone(resume_content)
    if not resume_embedding:
        return "Failed to generate embedding for the resume."

    try:
        query_response = index.query(
            vector=resume_embedding,
            top_k=10,
            include_metadata=True
        )

        matched_jobs = [
            {
                'job_id': match.id,
                'score': match.score,
                'title': match.metadata.get('title'),
                'company': match.metadata.get('company'),
                'description': match.metadata.get('description'),
                'compensation': match.metadata.get('compensation')
            }
            for match in query_response['matches']
        ]
        return matched_jobs

    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return f"An error occurred while matching jobs: {str(e)}"

# Example usage
original_resume = {
    "summary": "Experienced software developer...",
    "skills": "Python, JavaScript, React...",
    "experience": "Worked at XYZ Corp...",
    "education": "B.Sc in Computer Science",
    "projects": "Developed a resume builder..."
}

job_description = "Looking for a software engineer with experience in Python and React..."

rewritten_resume = rewrite_resume(original_resume, job_description)
print("Rewritten Resume:", rewritten_resume)

resume_content = "Experienced software developer proficient in Python and React, seeking a challenging position."
print("Resume content to be processed:", resume_content)  # Print for debugging
matched_jobs = match_jobs(resume_content)

print("Matched Jobs:", matched_jobs)
