from pinecone import Pinecone
from sentence_transformers import SentenceTransformer, util
import json
from bs4 import BeautifulSoup
from scrapfly import ScrapflyClient, ScrapeConfig

# Initialize Pinecone with your existing API key
pinecone_client = Pinecone(api_key='pcsk_qNsFT_HBcHa6jEqRq1YUzLbmSgNoZV8AfyrHmkK5dbKY9kXVLMtRQJCoHnQWrmdTLqf8s')

# Get the existing index (since it's already created)
index_name = "jobent"
index = pinecone_client.Index(index_name)

# Initialize Scrapfly client
SCRAPFLY_KEY = "scp-live-a7dc0dee17c24110a73d5d8cc82c7226"
client = ScrapflyClient(key=SCRAPFLY_KEY)

# Initialize embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# def extract_apollo_state(scrape_result):
#     try:
#         # Parse the HTML content
#         soup = BeautifulSoup(scrape_result.content, "html.parser")

#         # Find the Apollo state
#         script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
#         if not script_tag:
#             return {"error": "Apollo state not found in the page."}

#         # Load JSON data
#         apollo_state = json.loads(script_tag.string)

#         # Debugging: print the entire Apollo state to understand its structure
#         # print(json.dumps(apollo_state, indent=2))

#         # Extract jobs from the Apollo state
#         jobs = []

#         # Loop over the "apolloState" and look for highlightedJobListings
#         apollo_data = apollo_state.get("props", {}).get("pageProps", {}).get("apolloState", {})
#         for key, value in apollo_data.items():
#             # Check if the current key is a job listing reference (JobListingSearchResult)
#             if key.startswith("JobListingSearchResult:"):
#                 job_details = value

#                 # Create the job dictionary with the relevant details
#                 job = {
#                     "title": job_details.get("title", ""),
#                     "company": job_details.get("company", {}).get("name", ""),
#                     "description": job_details.get("description", ""),
#                     "location": job_details.get("locationNames", [])[0] if job_details.get("locationNames") else "",
#                     "url": f"https://wellfound.com/job/{job_details.get('slug', '')}",
#                     "jobType": job_details.get("jobType", ""),
#                     "compensation": job_details.get("compensation", ""),
#                     "yearsExperienceMin": job_details.get("yearsExperienceMin", ""),
#                     "yearsExperienceMax": job_details.get("yearsExperienceMax", ""),
#                 }
#                 jobs.append(job)
#                 print(f"Job found: {job}")


#         return jobs if jobs else {"error": "No jobs found in Apollo state."}
#     except Exception as e:
#         return {"error": f"Failed to extract jobs: {str(e)}"}


# def scrape_jobs(role="", location=""):
#     if role and location:
#         url = f"https://wellfound.com/role/l/{role}/{location}"
#     elif role:
#         url = f"https://wellfound.com/role/{role}"
#     elif location:
#         url = f"https://wellfound.com/location/{location}"
#     else:
#         raise ValueError("Either role or location must be provided.")
    
#     try:
#         result = client.scrape(ScrapeConfig(url=url, asp=True))
#         job_data = extract_apollo_state(result)
#         return job_data
#     except Exception as e:
#         return {"error": f"Scraping failed: {str(e)}"}

# def match_jobs_with_resume(resume_content, role="python-developer", location="san-francisco"):
#     try:
#         # Scrape jobs
#         jobs = scrape_jobs(role, location)
#         if "error" in jobs:
#             return jobs

#         # Embed the resume
#         resume_embedding = model.encode(resume_content)

#         # Embed job descriptions and find matches
#         job_matches = []
#         for job in jobs:
#             job_description = job.get("description", "")
#             job_embedding = model.encode(job_description)

#             # Compute similarity
#             similarity = util.cos_sim(resume_embedding, job_embedding).item()
#             job["similarity"] = similarity
#             job_matches.append(job)

#         # Sort by similarity score
#         job_matches.sort(key=lambda x: x["similarity"], reverse=True)

#         return job_matches[:10]
#     except Exception as e:
#         return {"error": f"Matching failed: {str(e)}"}


def extract_apollo_state(scrape_result):
    try:
        # Parse the HTML content
        soup = BeautifulSoup(scrape_result.content, "html.parser")

        # Find the Apollo state
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        if not script_tag:
            # print("Apollo state not found in the page.")
            return {"error": "Apollo state not found in the page."}

        # Load JSON data
        try:
            apollo_state = json.loads(script_tag.string)
            # print("Apollo state successfully loaded.")
            # print("Apollo state:", apollo_state)
        except json.JSONDecodeError as e:
            # print(f"Failed to decode JSON: {e}")
            return {"error": "Failed to decode JSON."}

        # Extract jobs from the Apollo state
        jobs = []

        # Loop over the "apolloState" and look for highlightedJobListings
        apollo_data = apollo_state.get("props", {}).get("pageProps", {}).get("apolloState", {})
        if not apollo_data:
            # print("No apolloState found in the parsed Apollo state.")
            return {"error": "No apolloState found in the parsed data."}
        
        # print(f"Apollo state contains {len(apollo_data)} entries.")
        # print("Apollo state keys:", apollo_data.keys()) 

        for key, value in apollo_data.items():
            # print(f"Key: {key}, Value: {value}")
            if key.startswith("JobListingSearchResult:"):
                job_details = value

                # Create the job dictionary with the relevant details
                job = {
                    "title": job_details.get("title", ""),
                    "company": job_details.get("company", {}).get("name", ""),
                    "description": job_details.get("description", ""),
                    "location": job_details.get("locationNames", [])[0] if job_details.get("locationNames") else "",
                    "url": f"https://wellfound.com/job/{job_details.get('slug', '')}",
                    "jobType": job_details.get("jobType", ""),
                    "compensation": job_details.get("compensation", ""),
                    "yearsExperienceMin": job_details.get("yearsExperienceMin", ""),
                    "yearsExperienceMax": job_details.get("yearsExperienceMax", ""),
                    "primaryRoleTitle": job_details.get("primaryRoleTitle", ""),
                    "remote": job_details.get("remote", False),
                    "slug": job_details.get("slug", ""),
                    "id": job_details.get("id", ""),
                    "isBookmarked": job_details.get("isBookmarked", False),
                    "companySize": job_details.get("companySize", ""),
                    "highConcept": job_details.get("highConcept", ""),
                    "logoUrl": job_details.get("logoUrl", ""),
                }
                jobs.append(job)
                print(f"Job found: {job}")

        if not jobs:
            # print("No jobs found in Apollo state.")
            return {"error": "No jobs found in Apollo state."}

        return jobs
    except Exception as e:
        # print(f"Failed to extract jobs: {str(e)}")
        return {"error": f"Failed to extract jobs: {str(e)}"}

def scrape_jobs(role="", location=""):
    if role and location:
        url = f"https://wellfound.com/role/l/{role}/{location}"
    elif role:
        url = f"https://wellfound.com/role/{role}"
    elif location:
        url = f"https://wellfound.com/location/{location}"
    else:
        raise ValueError("Either role or location must be provided.")
    
    try:
        result = client.scrape(ScrapeConfig(url=url, asp=True))
        job_data = extract_apollo_state(result)
        return job_data
    except Exception as e:
        return {"error": f"Scraping failed: {str(e)}"}

def match_jobs_with_resume(resume_content, role="python-developer", location="san-francisco"):
    try:
        # Scrape jobs
        jobs = scrape_jobs(role, location)
        if "error" in jobs:
            return jobs

        # Embed the resume
        resume_embedding = model.encode(resume_content)

        # Embed job descriptions and find matches
        job_matches = []
        for job in jobs:
            job_description = job.get("description", "")
            job_embedding = model.encode(job_description)

            # Compute similarity
            similarity = util.cos_sim(resume_embedding, job_embedding).item()
            job["similarity"] = similarity
            job_matches.append(job)

        # Sort by similarity score
        job_matches.sort(key=lambda x: x["similarity"], reverse=True)

        return job_matches[:10]
    except Exception as e:
        return {"error": f"Matching failed: {str(e)}"}

