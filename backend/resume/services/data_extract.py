import json
import requests
from django.http import JsonResponse
from django.shortcuts import redirect

# Helper to get cookie
def get_cookie(request, cookie_name):
    cookies = request.COOKIES
    return cookies.get(cookie_name)

# Helper to decode JWT token if Wellfound uses it
def decode_jwt(token):
    import base64
    try:
        base64_url = token.split('.')[1]  # Token is in three parts, base64_url is the second
        base64_str = base64_url.replace('-', '+').replace('_', '/')  # URL-safe base64 decoding
        decoded_bytes = base64.urlsafe_b64decode(base64_str + "==")
        decoded_str = decoded_bytes.decode('utf-8')
        return json.loads(decoded_str)  # Returns decoded JSON data
    except Exception as e:
        raise ValueError(f"Error decoding JWT token: {str(e)}")

# Redirect to Wellfound login page if the user is not logged in
def login_or_scrape(request):
    session_token = get_cookie(request, 'wellfound_session')  # Check if user is logged in
    
    if not session_token:
        # Redirect to Wellfound's login page
        return redirect("https://wellfound.com/login")
    
    # If user is logged in, proceed with scraping applications
    return scrape_applications(request)

# Scrape application data from Wellfound
def scrape_applications(request):
    try:
        session_token = get_cookie(request, 'wellfound_session')  # Get session cookie
        if not session_token:
            # If no session token, return error message
            return JsonResponse({"error": "User is not logged in to Wellfound"}, status=401)

        # Decode JWT token if necessary
        user_data = decode_jwt(session_token)
        user_id = user_data.get('user_id')  # Adjust according to the structure of the token
        if not user_id:
            return JsonResponse({"error": "User ID not found in session token"}, status=401)

        # Fetch application data based on the user_id
        application_data = fetch_user_applications(user_id)
        
        # Return data as a JsonResponse
        return JsonResponse(application_data, safe=False)  # Wrap the list of applications in a JsonResponse

    except Exception as e:
        # If an error occurs, return error message as JSON response
        error_message = {"error": f"Failed to scrape applications: {str(e)}"}
        return JsonResponse(error_message, status=500)

# Mock function to simulate fetching applications for the given user ID
def fetch_user_applications(user_id):
    # Replace with actual scraping logic or API call
    return [
        {"job_title": "Software Engineer", "company": "TechCorp", "status": "Applied"},
        {"job_title": "Data Scientist", "company": "DataX", "status": "Interview Scheduled"},
    ]
