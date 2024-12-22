# # from apify_client import ApifyClient

# # # Initialize Apify client with your API token
# # client = ApifyClient('apify_api_NdLf7nWOx4aUoeWjMx6A8rj4C5dVEi1UxkWx')

# # # Define the input for the scraper
# # run_input = {
# #     "listingStartUrls": [{"url": "https://wellfound.com/jobs"}],
# #     "jobsFilterFunction": "async ({ jobs }) => jobs.filter(({ published }) => ['today','yesterday','2 days ago','3 days ago','4 days ago','5 days ago','6 days ago','7 days ago'].includes(published))",
# #     "proxy": {
# #         "useApifyProxy": True  # Enables the Apify proxy
# #     }
# # }

# # # Run the scraper
# # run = client.actor('mscraper/wellfound-jobs-scraper').call(run_input=run_input)

# # # Check run status
# # print(f"Run status: {run['status']}")
# # if run['status'] != 'SUCCEEDED':
# #     print("Actor did not succeed. Check the input or Apify dashboard for errors.")
# #     exit()

# # # Retrieve the dataset items
# # dataset_items = client.dataset(run["defaultDatasetId"]).list_items().items
# # print(f"Number of jobs retrieved: {len(dataset_items)}")

# # if not dataset_items:
# #     print("No jobs found. Adjust your filters or verify the scraper is working correctly.")
# #     exit()

# # # Process the job listings
# # for item in dataset_items:
# #     print(f"Title: {item.get('title', 'N/A')}")
# #     print(f"Company: {item.get('company_name', 'N/A')}")
# #     print(f"Location: {item.get('location', 'N/A')}")
# #     print(f"Description: {item.get('description', 'N/A')}")
# #     print(f"URL: {item.get('url', 'N/A')}")
# #     print("-" * 40)



# from pinecone import Pinecone
# # import os

# # # Initialize Pinecone with the correct API key
# # pinecone = Pinecone(api_key="pcsk_DigCf_K19DeFaAr4MxYpebqg6qd2YjkvT3GJidqYmXL7QgVT5f7L2V6cjd846Ykhs3F92")

# # # Connect to your index
# # index_name = "jobent"
# # index = pinecone.Index(index_name)


# from sentence_transformers import SentenceTransformer

# # Initialize the embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# pc = Pinecone(api_key='pcsk_qNsFT_HBcHa6jEqRq1YUzLbmSgNoZV8AfyrHmkK5dbKY9kXVLMtRQJCoHnQWrmdTLqf8s')
# index = pc.Index("jobent")
# def upsert_job_vectors(jobs):
#     # Generate embeddings for each job description
#     vectors = []
#     for job in jobs:
#         job_description = job.get("description", "")
#         if not job_description:
#             continue  # Skip jobs without descriptions
        
#         # Create embedding for the job description
#         embedding = model.encode(job_description)
#         vectors.append({
#             "id": job["url"],  # Use job URL as the unique ID
#             "values": embedding,
#             "metadata": job  # Store job metadata for later retrieval
#         })

#     # Upsert the vectors into Pinecone
#     if vectors:
#         index.upsert(vectors)

# # Example usage with diverse job types
# jobs = [
#     {"title": "Python Developer", "company": "Company A", "description": "Develop Python applications", "location": "Remote", "url": "job-123"},
#     {"title": "Java Developer", "company": "Company B", "description": "Develop Java applications", "location": "New York", "url": "job-124"},
#     {"title": "Ruby on Rails Developer", "company": "Company C", "description": "Build web applications with Ruby", "location": "San Francisco", "url": "job-125"},
#     {"title": "Go Developer", "company": "Company D", "description": "Develop Go applications", "location": "Chicago", "url": "job-126"},
#     {"title": "JavaScript Developer", "company": "Company E", "description": "Build front-end web applications", "location": "Remote", "url": "job-127"}
# ]

# # Upsert jobs to Pinecone
# upsert_job_vectors(jobs)








# import time
# from selenium.webdriver.edge.service import Service as EdgeService
# from selenium.webdriver.edge.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver import Edge

# def wellfound_login():
#     """
#     Logs in to Wellfound using Selenium and waits for user to manually enter credentials.
#     """
#     # Configure Selenium options
#     edge_options = Options()
#     # edge_options.add_argument("--headless")  
#     edge_options.add_argument("--disable-gpu")
#     edge_options.add_argument("--no-sandbox")

#     # Set up the WebDriver
#     service = EdgeService(r"C:\Users\ishuv\Downloads\edgedriver_win64\msedgedriver.exe")
#     driver = Edge(service=service, options=edge_options)

#     try:
#         # Navigate to the Wellfound login page
#         print("Navigating to Wellfound login page...")
#         driver.get("https://wellfound.com/login")

#         # Wait for the page to load and for the cookie consent popup (if any)
#         wait = WebDriverWait(driver, 10)
        
#         # Accept cookie consent if available
#         try:
#             print("Checking for cookie consent popup...")
#             cookie_popup = WebDriverWait(driver, 5).until(
#                 EC.element_to_be_clickable((By.ID, "cookieConsentButton"))
#             )
#             cookie_popup.click()
#             print("Cookie consent accepted.")
#         except:
#             print("No cookie consent popup found.")

#         # Pause for user to manually fill in the login details
#         print("Please manually log in to Wellfound and press Enter when done.")
#         input("Press Enter after logging in manually...")

#         # After user logs in, verify login by checking for a dashboard element
#         print("Checking login status...")
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, "dashboard"))
#         )
#         print("Wellfound login successful.")
#         return driver

#     except Exception as e:
#         print(f"Error during login: {e}")
#         driver.quit()
#         return None

# if __name__ == "__main__":
#     # Step 1: Log in to Wellfound (user to fill credentials manually)
#     driver = wellfound_login()

#     if driver:
#         print("Successfully logged in!")
#         # You can now proceed with additional steps if needed
#         driver.quit()
#     else:
#         print("Login failed.")



# import time
# import random
# from selenium.webdriver.edge.service import Service as EdgeService
# from selenium.webdriver.edge.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver import Edge

# def human_like_delay(min_delay=1, max_delay=3):
#     """Introduce a random delay to simulate human-like behavior."""
#     time.sleep(random.uniform(min_delay, max_delay))

# def human_like_scroll(driver):
#     """Simulate scrolling down the page."""
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     human_like_delay(1, 3)

# def human_like_mouse_movement(driver):
#     """Simulate random mouse movements."""
#     driver.execute_script("window.scrollTo(0, 0);")  # simulate mouse going to top
#     human_like_delay(1, 2)

# def configure_driver():
#     """Configure the WebDriver with options like proxy rotation and JavaScript enablement."""
#     edge_options = Options()
    
#     # Add configurations for human-like interaction
#     edge_options.add_argument("--disable-gpu")  # Disable GPU acceleration
#     edge_options.add_argument("--no-sandbox")  # For running in restricted environments
#     edge_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection
    
#     # Optionally: Add proxy for IP rotation (replace with actual proxy if needed)
#     edge_options.add_argument('--proxy-server=http://52.73.224.54:3128')

    
#     return edge_options

# def wellfound_login():
#     """
#     Logs in to Wellfound using Selenium and waits for user to manually enter credentials.
#     """
#     # Set up the WebDriver
#     edge_options = configure_driver()
#     service = EdgeService(r"C:\Users\ishuv\Downloads\edgedriver_win64\msedgedriver.exe")
#     driver = Edge(service=service, options=edge_options)

#     try:
#         # Navigate to the Wellfound login page
#         print("Navigating to Wellfound login page...")
#         driver.get("https://wellfound.com/login")

#         # Wait for the page to load and for the cookie consent popup (if any)
#         wait = WebDriverWait(driver, 10)
        
#         # Accept cookie consent if available
#         try:
#             print("Checking for cookie consent popup...")
#             cookie_popup = WebDriverWait(driver, 5).until(
#                 EC.element_to_be_clickable((By.ID, "cookieConsentButton"))
#             )
#             cookie_popup.click()
#             print("Cookie consent accepted.")
#         except:
#             print("No cookie consent popup found.")

#         # Pause for user to manually fill in the login details
#         print("Please manually log in to Wellfound and press Enter when done.")
#         input("Press Enter after logging in manually...")

#         # After user logs in, verify login by checking for a dashboard element
#         print("Checking login status...")
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, "dashboard"))
#         )
#         print("Wellfound login successful.")

#         # Simulate human-like interactions (e.g., scrolling, mouse movements)
#         human_like_delay(1, 3)
#         human_like_scroll(driver)
#         human_like_mouse_movement(driver)
        
#         return driver

#     except Exception as e:
#         print(f"Error during login: {e}")
#         driver.quit()
#         return None

# def scrape_applications(driver):
#     """Scrape the job applications once logged in to Wellfound."""
#     try:
#         # Navigate to the job applications page
#         print("Navigating to job applications page...")
#         driver.get("https://wellfound.com/jobs/applications")
        
#         # Wait for the page to load and check for the applications
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "application-item"))
#         )
        
#         # Get all application items (jobs)
#         applications = driver.find_elements(By.CLASS_NAME, "application-item")
        
#         # Extract and print job titles and status
#         print(f"Found {len(applications)} applications.")
#         for app in applications:
#             title = app.find_element(By.CLASS_NAME, "job-title").text
#             status = app.find_element(By.CLASS_NAME, "status").text
#             print(f"Job Title: {title}, Status: {status}")

#         return len(applications)

#     except Exception as e:
#         print(f"Error while scraping applications: {e}")
#         return 0

# def clear_cookies(driver):
#     """Clear cookies to avoid getting flagged as a bot."""
#     driver.delete_all_cookies()

# if __name__ == "__main__":
#     # Step 1: Log in to Wellfound (user to fill credentials manually)
#     driver = wellfound_login()

#     if driver:
#         # Step 2: Once logged in, scrape job applications
#         num_applications = scrape_applications(driver)
#         print(f"Total applications: {num_applications}")

#         # Clear cookies after scraping
#         clear_cookies(driver)
        
#         # Optionally quit the driver if you're done
#         driver.quit()
#     else:
#         print("Login failed.")


# #prafulvats01@gmail.com
# #Forjobs@11



import json
import asyncio
from scrapfly import ScrapflyClient, ScrapeConfig

def extract_apollo_state(result):
    """
    Extracts the Apollo state (GraphQL data) from the Wellfound page.
    """
    data = result.selector.css("script#__NEXT_DATA__::text").get()
    data = json.loads(data)
    graph = data["props"]["pageProps"]["apolloState"]["data"]
    return graph

def unpack_node_references(node, graph):
    """
    Unpacks references in the Apollo state graph.
    Recursively fetches full node data from the graph.
    """
    def flatten(value):
        try:
            if value["type"] != "id":
                return value
        except (KeyError, TypeError):
            return value
        data = graph[value["id"]]
        if data.get("node"):
            data = flatten(data["node"])
        return data

    node = flatten(node)

    for key, value in node.items():
        if isinstance(value, list):
            node[key] = [flatten(v) for v in value]
        elif isinstance(value, dict):
            node[key] = unpack_node_references(value, graph)
    return node

async def scrape_wellfound_jobs(session: ScrapflyClient, role: str = "", location: str = ""):
    """
    Scrapes Wellfound for job listings by role and location.
    Returns a list of companies with job details.
    """
    if role and location:
        url = f"https://wellfound.com/role/l/{role}/{location}"
    elif role:
        url = f"https://wellfound.com/role/{role}"
    elif location:
        url = f"https://wellfound.com/location/{location}"
    else:
        raise ValueError("Need to pass either role or location argument to scrape search")

    scrape = ScrapeConfig(url=url, asp=True)
    result = await session.async_scrape(scrape)
    graph = extract_apollo_state(result)

    companies = []
    for key in graph:
        if key.startswith("StartupResult"):
            company_data = unpack_node_references(graph[key], graph)
            companies.append(company_data)
    
    return companies

def display_companies(companies):
    """
    Displays the company and job details in a readable format in the terminal.
    """
    for company in companies:
        print(f"\nCompany: {company.get('name', 'N/A')}")
        print(f"Size: {company.get('companySize', 'N/A')}")
        print(f"Concept: {company.get('highConcept', 'N/A')}")
        print(f"Logo URL: {company.get('logoUrl', 'N/A')}")
        
        for job in company.get("highlightedJobListings", []):
            print(f"\n  Job Title: {job.get('title', 'N/A')}")
            print(f"  Location: {', '.join(job.get('locationNames', {}).get('json', []))}")
            print(f"  Compensation: {job.get('compensation', 'N/A')}")
            print(f"  Job Type: {job.get('jobType', 'N/A')}")
            print(f"  Description: {job.get('description', 'N/A')}\n")
        
        print("="*50)

if __name__ == "__main__":
    # Set your Scrapfly API key
    with ScrapflyClient(key="scp-live-a7dc0dee17c24110a73d5d8cc82c7226", max_concurrency=2) as session:
        # Run the scrape job with desired role and location
        result = asyncio.run(scrape_wellfound_jobs(session, role="python-developer", location="san-francisco"))
        # Display the results
        display_companies(result)
