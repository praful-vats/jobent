import time
import json
import sys
from datetime import datetime
from collections import namedtuple
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from django.conf import settings

# Initialize Pinecone using the new class-based method
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Create the index instance
index = pc.Index(settings.PINECONE_INDEX_NAME)

# Initialize Sentence-Transformers model
model = SentenceTransformer('all-MiniLM-L6-v2')  # You can use a different model if you prefer

now = datetime.now()
date_time_format = now.strftime("%Y-%m-%d_%H-%M-%S")

JobListingSearchResult = namedtuple(
    "JobListingSearchResult",
    [
        "typename", "atsSource", "autoPosted", "currentUserApplied", "description", "id", "jobType",
        "lastRespondedAt", "liveStartAt", "primaryRoleTitle", "remote", "reposted", "slug",
        "title", "compensation", "usesEstimatedSalary",
    ],
)

class Companies:
    def __init__(self, query=[]):
        self.query = query

    def embed_text(self, text):
        """
        Generate embedding for the input text using the Sentence-Transformers model.
        """
        if isinstance(text, str) and text.strip():  # Ensure text is a valid string and not empty
            try:
                # Generate the embedding
                embedding = model.encode(text)
                return embedding
            except Exception as e:
                print(f"Error generating embedding: {e}")
                return None
        else:
            print("Error: Input text is invalid or empty.")
            return None


    def get_companies(self, query):
        job_listings = []
        for i in range(1, 100):
            js_script = self.create_js_script(i)
            response = self.execute_js_script(js_script)

            if response:
                new_listings = self.process_response(response)
                job_listings.extend(new_listings)
                self.save_response_to_file(response, i)

                if not response["data"]["talent"]["jobSearchResults"]["hasNextPage"]:
                    break

            self.wait_between_requests()

        return job_listings

    def create_js_script(self, page):
        return f"""
        var callback = arguments[0];
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'https://wellfound.com/graphql?fallbackAOR=talent', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.setRequestHeader('Accept', '*/*');
        xhr.setRequestHeader('Accept-Encoding', 'gzip, deflate, br, zstd');
        xhr.setRequestHeader('Accept-Language', 'en-US,en;q=0.9');
        xhr.setRequestHeader('Apollographql-Client-Name', 'talent-web');
        xhr.setRequestHeader('Origin', 'https://wellfound.com');
        xhr.setRequestHeader('Referer', 'https://wellfound.com/jobs');
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.onreadystatechange = function() {{
            if (xhr.readyState == 4) {{
                if (xhr.status == 200) {{
                    callback(xhr.responseText);
                }} else {{
                    console.error("Error with status code:", xhr.status);
                    callback("Error: " + xhr.statusText);
                }}
            }}
        }}; 
        xhr.send(JSON.stringify({{
            "operationName": "JobSearchResultsX",
            "variables": {{
                "filterConfigurationInput": {{
                    "page": {page},
                    "remoteCompanyLocationTagIds": ["1692", "1693"],
                    "roleTagIds": ["14726"],
                    "skillTagIds": ["14775", "139914", "17000"],
                    "excludedKeywords": ["web3", "crypto", "cryptocurrency"],
                    "jobTypes": ["full_time"],
                    "remotePreference": "REMOTE_OPEN",
                }}
            }},
            "extensions": {{
                "operationId": "tfe/b898ee628dd3385e1b8c467e464a0261ad66c478eda6e21e10566b0ca4ccf1e9"
            }}
        }}));
        """

    def execute_js_script(self, js_script):
        # This method should execute the provided JavaScript in a browser or WebDriver.
        # Implement using a library like Selenium if required.
        raise NotImplementedError("execute_js_script needs to be implemented")

    def process_response(self, response):
        job_listings = []
        startups = response["data"]["talent"]["jobSearchResults"]["startups"]["edges"]
        for startup in startups:
            startup_info = startup["node"]
            startup_job_listings = startup_info["highlightedJobListings"]
            for job in startup_job_listings:
                job_listing = JobListingSearchResult(
                    job["__typename"], job["atsSource"], job["autoPosted"], job["currentUserApplied"],
                    job["description"], job["id"], job["jobType"], job["lastRespondedAt"],
                    job["liveStartAt"], job["primaryRoleTitle"], job["remote"], job["reposted"],
                    job["slug"], job["title"], job["compensation"], job["usesEstimatedSalary"]
                )
                job_listings.append(job_listing)
                print(f"{job_listing.title} | {job_listing.compensation} | {job_listing.id}")

                # Index the job in Pinecone
                job_embedding = self.embed_text(job_listing.description)
                if job_embedding is not None:
                    index.upsert([(job_listing.id, job_embedding, {
                        'title': job_listing.title,
                        'company': startup_info['name'],
                        'description': job_listing.description,
                        'compensation': job_listing.compensation
                    })])

        return job_listings

    def save_response_to_file(self, response, page_number):
        response_json = json.dumps(response, indent=4)
        with open(f"response_{date_time_format}_page_{page_number}.json", "w") as file:
            print("Writing to file...")
            file.write(response_json)

    def wait_between_requests(self):
        for remaining in range(10, 0, -1):
            sys.stdout.write(f"\rSleeping in {remaining} seconds...")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write("\rComplete!\n")

    def match_jobs_with_resume(self, resume_content):
        """
        Matches jobs from Wellfound based on the resume content.
        """
        # Embed the resume content
        resume_embedding = self.embed_text(resume_content)
        
        if not resume_embedding:
            return {"error": "Failed to generate embedding for the resume"}

        # Scrape Wellfound and index jobs
        self.scrape_and_index_jobs()  # Fetch and index job listings in Pinecone

        # Query Pinecone for matching jobs
        matched_jobs = self.query_jobs(resume_embedding)

        return matched_jobs

    def query_jobs(self, resume_embedding):
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
            return {"error": f"An error occurred while matching jobs: {str(e)}"}


def scrape_and_index_jobs():
    companies = Companies()
    job_listings = companies.get_companies(query=[])

    for job in job_listings:
        job_embedding = companies.embed_text(job.description)
        if job_embedding is not None:
            index.upsert([(job.id, job_embedding, {
                'title': job.title,
                'company': job.company,
                'description': job.description,
                'compensation': job.compensation
            })])

def match_jobs_with_resume(resume_content):
    companies = Companies()
    resume_embedding = companies.embed_text(resume_content)
    matched_jobs = companies.match_jobs_with_resume(resume_embedding)

    return matched_jobs
