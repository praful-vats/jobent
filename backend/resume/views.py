from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Resume
from .serializers import ResumeSerializer
from users.models import UserProfile
from resume.services.groq_api import rewrite_resume
from resume.services.groq_api import generate_cover_letter
from io import BytesIO
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.pdfgen import canvas # type: ignore
import PyPDF2 # type: ignore
from rest_framework.parsers import MultiPartParser, FormParser
import logging
import re
import os
import fitz  #type: ignore
from django.conf import settings
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.pdfgen import canvas # type: ignore
from django.urls import reverse
from django.http import JsonResponse
from resume.services.data_extract import scrape_applications
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from resume.services.job_matching import match_jobs_with_resume
from resume.services.bot import process_conversation
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_file_path):
    """
    Extract structured text content from a PDF file, preserving key sections.
    """
    with open(pdf_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        # Example: Splitting content into sections (you can customize based on your structure)
        sections = {
            "summary": "",
            "skills": "",
            "experience": "",
            "education": "",
            "projects": ""
        }
        
        # A basic example of regex-based section extraction (you can modify this based on your content)
        sections["summary"] = re.search(r"Summary.*?(?=\n\n|\Z)", text, re.DOTALL)
        sections["skills"] = re.search(r"Skills.*?(?=\n\n|\Z)", text, re.DOTALL)
        sections["experience"] = re.search(r"Experience.*?(?=\n\n|\Z)", text, re.DOTALL)
        sections["education"] = re.search(r"Education.*?(?=\n\n|\Z)", text, re.DOTALL)
        sections["projects"] = re.search(r"Projects.*?(?=\n\n|\Z)", text, re.DOTALL)
        
        # Returning the structured sections
        return {key: section.group(0) if section else "" for key, section in sections.items()}


# class ResumeUploadView(ListCreateAPIView):
#     """
#     View to upload and list resumes.
#     """
#     permission_classes = [IsAuthenticated]
#     queryset = Resume.objects.all()
#     serializer_class = ResumeSerializer
#     parser_classes = (MultiPartParser, FormParser)

#     def perform_create(self, serializer):
#         user = self.request.user
#         # Delete all old resumes of the user before uploading the new one
#         Resume.objects.filter(user=user).delete()

#         # Create and save the new resume
#         resume = serializer.save(user=user, is_latest=True)
        
#         # Ensure that file_name is set after saving the resume
#         if resume.file:
#             resume.file_name = resume.file.name
#             resume.save()

#     def create(self, request, *args, **kwargs):
#         logger.debug("Received request to upload resume")
#         try:
#             response = super().create(request, *args, **kwargs)
#             resume_id = response.data.get('id')
#             if not resume_id:
#                 logger.error("Resume ID not found in response data")
#                 return Response(
#                     {"error": "Resume ID not found in response data"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             resume = Resume.objects.get(pk=resume_id)
#             if resume.file.name.endswith(".pdf"):
#                 resume.content = extract_text_from_pdf(resume.file.path)
#             else:
#                 try:
#                     resume.content = resume.file.read().decode("utf-8", errors="replace")
#                 except Exception as e:
#                     logger.error(f"Failed to read resume file: {str(e)}")
#                     return Response(
#                         {"error": f"Failed to read resume file: {str(e)}"},
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )
#             resume.save()
#             logger.debug("Resume uploaded and processed successfully")
#             return response
#         except Exception as e:
#             logger.error(f"Failed to upload resume: {str(e)}")
#             return Response(
#                 {"error": f"Failed to upload resume: {str(e)}"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

class ResumeUploadView(ListCreateAPIView):
    """
    View to upload and list resumes.
    """
    permission_classes = [IsAuthenticated]
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def perform_create(self, serializer):
        user = self.request.user
        
        # Ensure user has a profile before creating a resume
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # Delete all old resumes of the user before uploading the new one
        Resume.objects.filter(user=user).delete()

        # Create and save the new resume
        resume = serializer.save(user=user, is_latest=True)

        # Ensure that file_name is set after saving the resume
        if resume.file:
            resume.file_name = resume.file.name
            resume.save()

    def create(self, request, *args, **kwargs):
        logger.debug("Received request to upload resume")
        try:
            response = super().create(request, *args, **kwargs)
            resume_id = response.data.get('id')
            if not resume_id:
                logger.error("Resume ID not found in response data")
                return Response(
                    {"error": "Resume ID not found in response data"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            resume = Resume.objects.get(pk=resume_id)
            if resume.file.name.endswith(".pdf"):
                resume.content = self.extract_text_from_pdf(resume.file.path)
            else:
                try:
                    resume.content = resume.file.read().decode("utf-8", errors="replace")
                except Exception as e:
                    logger.error(f"Failed to read resume file: {str(e)}")
                    return Response(
                        {"error": f"Failed to read resume file: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            resume.save()
            logger.debug("Resume uploaded and processed successfully")
            return response
        except Exception as e:
            logger.error(f"Failed to upload resume: {str(e)}")
            return Response(
                {"error": f"Failed to upload resume: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def extract_text_from_pdf(self, pdf_file_path):
        """
        Extract structured text content from a PDF file, preserving key sections.
        """
        with open(pdf_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()

            # Example: Splitting content into sections (you can customize based on your structure)
            sections = {
                "summary": "",
                "skills": "",
                "experience": "",
                "education": "",
                "projects": ""
            }

            # A basic example of regex-based section extraction (you can modify this based on your content)
            sections["summary"] = re.search(r"Summary.*?(?=\n\n|\Z)", text, re.DOTALL)
            sections["skills"] = re.search(r"Skills.*?(?=\n\n|\Z)", text, re.DOTALL)
            sections["experience"] = re.search(r"Experience.*?(?=\n\n|\Z)", text, re.DOTALL)
            sections["education"] = re.search(r"Education.*?(?=\n\n|\Z)", text, re.DOTALL)
            sections["projects"] = re.search(r"Projects.*?(?=\n\n|\Z)", text, re.DOTALL)

            # Returning the structured sections
            return {key: section.group(0) if section else "" for key, section in sections.items()}


class ResumeListView(APIView):
    """
    View to list all resumes for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        resumes = Resume.objects.filter(user=user)  # Fetch only user's resumes
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def extract_layout_from_pdf(pdf_file_path):
    doc = fitz.open(pdf_file_path)
    layout = []

    # Extract layout information for each page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if block['type'] == 0:  # Only text blocks (ignore images, lines, etc.)
                text = block.get('text', '')  # Safely get 'text' if it exists
                if text.strip():  # Only include non-empty text blocks
                    layout.append({
                        'text': text,
                        'bbox': block.get('bbox', (0, 0, 0, 0)),  # Bounding box (x0, y0, x1, y1)
                        'font': block.get('font', 'Helvetica'),  # Example, use the actual font
                    })
    return layout

class ResumeRewriteView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user

        # Fetch the user's latest resume
        try:
            resume = Resume.objects.get(user=user, is_latest=True)
        except Resume.DoesNotExist:
            return Response(
                {"error": "No latest resume found for the user."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get the job description from the request
        job_description = request.data.get("job_description")
        if not job_description:
            return Response(
                {"error": "Job description is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract text content from the resume
        file_content = None
        if resume.file.name.endswith(".pdf"):
            file_content = extract_text_from_pdf(resume.file.path)
        else:
            try:
                file_content = resume.file.read().decode("utf-8", errors="replace")
            except Exception as e:
                return Response(
                    {"error": f"Failed to read resume file: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if not file_content:
            return Response(
                {"error": "Failed to extract text from the resume."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Call the resume rewriting service
        rewritten_resume = rewrite_resume(file_content, job_description)
        if not rewritten_resume:
            return Response(
                {"error": "Failed to rewrite resume."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Call the cover letter generation service
        cover_letter = generate_cover_letter(rewritten_resume, job_description)
        if not cover_letter:
            return Response(
                {"error": "Failed to generate cover letter."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Deduct one token for premium users
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.user_type == "premium":
            user_profile.premium_tokens -= 1
            user_profile.save()

        # Generate PDFs for the rewritten resume and cover letter
        resume_pdf_path = os.path.join(settings.MEDIA_ROOT, 'resumes', f"rewritten_resume_{resume.id}.pdf")
        cover_letter_pdf_path = os.path.join(settings.MEDIA_ROOT, 'resumes', f"cover_letter_{resume.id}.pdf")
        self.create_pdf(resume_pdf_path, rewritten_resume)
        self.create_pdf(cover_letter_pdf_path, cover_letter)

        resume_file_url = reverse('resume:download', kwargs={'file_name': f"rewritten_resume_{resume.id}.pdf"})
        cover_letter_file_url = reverse('resume:download', kwargs={'file_name': f"cover_letter_{resume.id}.pdf"})

        return Response({
            "message": "Resume and cover letter generated successfully",
            "resume_file_url": resume_file_url,
            "cover_letter_file_url": cover_letter_file_url
        })

    def create_pdf(self, output_path, content):
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        y_position = height - 50  # Start at the top of the page
        for line in content.split("\n"):
            if y_position < 50:  # Start a new page if near the bottom
                c.showPage()
                y_position = height - 50
            c.drawString(50, y_position, line)
            y_position -= 12  # Adjust line spacing

        c.save()




def download_resume(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'resumes', file_name)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf', as_attachment=True)
    else:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)


class JobMatchingView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        try:
            resume = Resume.objects.get(user=user, is_latest=True)
        except Resume.DoesNotExist:
            return Response({"error": "No latest resume found."}, status=status.HTTP_404_NOT_FOUND)

        # Step 2: Extract text from the resume (assuming it's a PDF)
        resume_content = """Highly motivated and detail-oriented software engineer with experience in developing web applications, 
        and a strong background in Python, Django, and React. Looking for opportunities to leverage expertise 
        in full-stack development to contribute to innovative tech teams."""

        # Match jobs with the resume
        matched_jobs = match_jobs_with_resume(resume_content)
        print("Matched jobs:", matched_jobs)

        if "error" in matched_jobs:
            return Response(matched_jobs, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not matched_jobs:
            return Response({"message": "No jobs matched your resume."}, status=status.HTTP_200_OK)

        return Response(matched_jobs, status=status.HTTP_200_OK)

from resume.services.data_extract import scrape_applications

def extract_applications_view(request):
    try:
        # Call the scrape_applications function to get data
        application_data = scrape_applications(request)

        # Check if the scrape_applications function returned an error
        if "error" in application_data:
            return JsonResponse(application_data, status=400)

        # Return the scraped data as JSON response
        return JsonResponse(application_data, safe=False)
    
    except Exception as e:
        # Handle any errors that occur during the scraping
        return JsonResponse({"error": f"Failed to extract applications: {str(e)}"}, status=500)

def perform_create(self, serializer):
    user = self.request.user

    # Fetch and delete old resumes and their associated files
    old_resumes = Resume.objects.filter(user=user)
    for old_resume in old_resumes:
        if old_resume.file:
            try:
                if os.path.exists(old_resume.file.path):
                    os.remove(old_resume.file.path)
                    print(f"Deleted old file: {old_resume.file.path}")
                else:
                    print(f"File not found: {old_resume.file.path}")
            except Exception as e:
                print(f"Error deleting file {old_resume.file.path}: {str(e)}")

    # Delete old resume records
    old_resumes.delete()

    # Create and save the new resume
    resume = serializer.save(user=user, is_latest=True)
    if resume.file:
        resume.file_name = resume.file.name
        resume.content = resume.extract_text_from_file()  # Extract text from the uploaded file
        resume.save()

# @csrf_exempt

# # Handle cases where the request is not POST
# def chat_view(request):
#     if request.method == 'POST':
#         # Read the JSON body of the request
#         try:
#             data = json.loads(request.body)
#             user_input = data.get('user_input', '')
            
#             if user_input:
#                 # Get the bot's reply
#                 reply = process_conversation(user_input)
#                 return JsonResponse({'reply': reply})
#             else:
#                 return JsonResponse({'error': 'No user input provided'}, status=400)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
#     # Return a 405 if method is not POST
#     return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


# class chat_view(APIView):
#     permission_classes = [IsAuthenticated]  # Ensure user is authenticated
    
#     def post(self, request):
#         """
#         Handle POST request for chat interaction, process user input, and return bot reply.
#         """
#         print("Authorization Header:", request.headers.get('Authorization'))

#         # Get the user from the authenticated request
#         user = request.user
#         user_id = user.id

#         # Check if there's any input from the user
#         try:
#             data = json.loads(request.body)
#             user_input = data.get('user_input', '')

#             if not user_input:
#                 return JsonResponse({'error': 'No user input provided'}, status=400)

#             # Initialize or retrieve conversation history for the user in the session
#             if 'conversation_history' not in request.session:
#                 request.session['conversation_history'] = {}

#             if user_id not in request.session['conversation_history']:
#                 request.session['conversation_history'][user_id] = []

#             # Retrieve the conversation history
#             conversation_history = request.session['conversation_history'][user_id]

#             # Process user input and get the bot's reply
#             reply = process_conversation(user_input, user_id, conversation_history)

#             # Update the conversation history with the new user input and bot reply
#             request.session['conversation_history'][user_id].append({'question': user_input, 'reply': reply})
#             request.session.modified = True  # Ensure the session is saved
#             request.session.save()  # Force session save
#             print("Session data after saving:", request.session.get('conversation_history'))
#             return JsonResponse({'reply': reply})

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)


#     def get(self, request):
#         """
#         Handle GET request to fetch the most recent conversation.
#         """
#         print("Request received at GET endpoint.")
        
#         user = request.user
#         user_id = user.id

#         if 'conversation_history' not in request.session:
#             return JsonResponse({'error': 'No conversation history found'}, status=404)

#         conversation_history = request.session['conversation_history'].get(user_id, [])

#         if conversation_history:
#             # Return the most recent conversation
#             recent_conversation = conversation_history[-1]
#             return JsonResponse({
#                 'question': recent_conversation['question'],
#                 'reply': recent_conversation['reply']
#             })
#         else:
#             return JsonResponse({'error': 'No conversation history found'}, status=404)

from .models import Conversation
class chat_view(APIView):
    permission_classes = [IsAuthenticated]  # Ensure user is authenticated

    def post(self, request):
        """
        Handle POST request for chat interaction, process user input, and return bot reply.
        """
        user = request.user
        user_input = request.data.get('user_input', '')

        if not user_input:
            return JsonResponse({'error': 'No user input provided'}, status=400)

        # Fetch the user's previous conversation history
        conversation_history = Conversation.objects.filter(user=user).order_by('timestamp')

        # Process the conversation (pass user input, user ID, and conversation history)
        reply = process_conversation(user_input, user.id, conversation_history)

        # Save the conversation to the database
        Conversation.objects.create(
            user=user,
            question=user_input,
            reply=reply
        )

        return JsonResponse({'reply': reply})

    def get(self, request):
        """
        Handle GET request to fetch the most recent conversation.
        """
        user = request.user

        # Retrieve the most recent conversation
        conversation = Conversation.objects.filter(user=user).order_by('-timestamp').first()

        if conversation:
            return JsonResponse({
                'question': conversation.question,
                'reply': conversation.reply
            })
        else:
            return JsonResponse({'error': 'No conversation history found'}, status=404)