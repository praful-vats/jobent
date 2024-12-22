# from apify_client import ApifyClient

# # Initialize Apify client with your API token
# client = ApifyClient('apify_api_NdLf7nWOx4aUoeWjMx6A8rj4C5dVEi1UxkWx')

# # Define the input for the scraper
# run_input = {
#     "listingStartUrls": [{"url": "https://wellfound.com/jobs"}],
#     "jobsFilterFunction": "async ({ jobs }) => jobs.filter(({ published }) => ['today','yesterday','2 days ago','3 days ago','4 days ago','5 days ago','6 days ago','7 days ago'].includes(published))",
#     "proxy": {
#         "useApifyProxy": True  # Enables the Apify proxy
#     }
# }

# # Run the scraper
# run = client.actor('mscraper/wellfound-jobs-scraper').call(run_input=run_input)

# # Check run status
# print(f"Run status: {run['status']}")
# if run['status'] != 'SUCCEEDED':
#     print("Actor did not succeed. Check the input or Apify dashboard for errors.")
#     exit()

# # Retrieve the dataset items
# dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items
# print(f"Number of jobs retrieved: {len(dataset_items)}")

# if not dataset_items:
#     print("No jobs found. Adjust your filters or verify the scraper is working correctly.")
#     exit()

# # Process the job listings
# for item in dataset_items:
#     print(f"Title: {item.get('title', 'N/A')}")
#     print(f"Company: {item.get('company_name', 'N/A')}")
#     print(f"Location: {item.get('location', 'N/A')}")
#     print(f"Description: {item.get('description', 'N/A')}")
#     print(f"URL: {item.get('url', 'N/A')}")
#     print("-" * 40)



from pinecone import Pinecone
# import os

# # Initialize Pinecone with the correct API key
# pinecone = Pinecone(api_key="pcsk_DigCf_K19DeFaAr4MxYpebqg6qd2YjkvT3GJidqYmXL7QgVT5f7L2V6cjd846Ykhs3F92")

# # Connect to your index
# index_name = "jobent"
# index = pinecone.Index(index_name)


from sentence_transformers import SentenceTransformer

# Initialize the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

pc = Pinecone(api_key='pcsk_qNsFT_HBcHa6jEqRq1YUzLbmSgNoZV8AfyrHmkK5dbKY9kXVLMtRQJCoHnQWrmdTLqf8s')
index = pc.Index("jobent")
def upsert_job_vectors(jobs):
    # Generate embeddings for each job description
    vectors = []
    for job in jobs:
        job_description = job.get("description", "")
        if not job_description:
            continue  # Skip jobs without descriptions
        
        # Create embedding for the job description
        embedding = model.encode(job_description)
        vectors.append({
            "id": job["url"],  # Use job URL as the unique ID
            "values": embedding,
            "metadata": job  # Store job metadata for later retrieval
        })

    # Upsert the vectors into Pinecone
    if vectors:
        index.upsert(vectors)

# Example usage with diverse job types
jobs = [
    {"title": "Python Developer", "company": "Company A", "description": "Develop Python applications", "location": "Remote", "url": "job-123"},
    {"title": "Java Developer", "company": "Company B", "description": "Develop Java applications", "location": "New York", "url": "job-124"},
    {"title": "Ruby on Rails Developer", "company": "Company C", "description": "Build web applications with Ruby", "location": "San Francisco", "url": "job-125"},
    {"title": "Go Developer", "company": "Company D", "description": "Develop Go applications", "location": "Chicago", "url": "job-126"},
    {"title": "JavaScript Developer", "company": "Company E", "description": "Build front-end web applications", "location": "Remote", "url": "job-127"}
]

# Upsert jobs to Pinecone
upsert_job_vectors(jobs)
