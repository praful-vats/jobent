from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from django.http import FileResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Resume
from .serializers import ResumeSerializer
from users.models import UserProfile
from backend.resume.services.resume_modifier import rewrite_resume
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
from resume.services.job_matching import match_jobs

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


class ResumeUploadView(ListCreateAPIView):
    """
    View to upload and list resumes.
    """
    permission_classes = [IsAuthenticated]
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        user = self.request.user
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
                resume.content = extract_text_from_pdf(resume.file.path)
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

        # Fetch the user's profile
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response(
                {"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Fetch the latest resume instance (marked as is_latest=True)
        try:
            resume = Resume.objects.get(user=user, is_latest=True)
        except Resume.DoesNotExist:
            return Response(
                {"error": "No latest resume found for the user."}, status=status.HTTP_404_NOT_FOUND
            )

        job_description = request.data.get("job_description")

        if not job_description:
            return Response(
                {"error": "Job description is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Extract layout from the original PDF
        layout = extract_layout_from_pdf(resume.file.path)

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

        # Call the Groq API to rewrite the resume
        rewritten_resume = rewrite_resume(file_content, job_description)

        if not rewritten_resume:
            return Response(
                {"error": "Failed to rewrite resume."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Deduct one token if the user is premium
        if profile.user_type == "premium":
            profile.premium_tokens -= 1
            profile.save()

        # Generate the rewritten resume as a PDF with the same layout
        # Define the output path using the user's latest resume's id
        output_pdf_dir = os.path.join(settings.MEDIA_ROOT, 'resumes')
        os.makedirs(output_pdf_dir, exist_ok=True)  # Ensure the directory exists

        output_pdf_path = os.path.join(output_pdf_dir, f"rewritten_resume_{resume.id}.pdf")

        # Generate the PDF with the rewritten content
        self.create_rewritten_pdf(output_pdf_path, rewritten_resume, layout)

        file_url = reverse('resume:download', kwargs={'file_name': f"rewritten_resume_{resume.id}.pdf"})

        # Return the new PDF file as a response
        return Response({
            'message': 'Resume rewritten successfully',
            'file_url': file_url
        })

    def create_rewritten_pdf(self, output_path, rewritten_resume, original_layout):
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        y_position = height - 50  # Start position (from top of the page)

        # Ensure rewritten_resume is a string before splitting it into lines
        if isinstance(rewritten_resume, tuple):
            rewritten_resume = rewritten_resume[0]  # Extract the actual resume content if it's a tuple

        rewritten_lines = rewritten_resume.split("\n")  # Now we can safely split

        # Add text with original layout info
        def add_text(text, y_position, font="Helvetica", font_size=10):
            c.setFont(font, font_size)
            c.drawString(50, y_position, text)
            return y_position - font_size - 2  # Adjust the y position after adding text

        for line in rewritten_lines:
            # You can adjust this logic to more closely match the original layout
            y_position = add_text(line, y_position)
            if y_position < 50:
                c.showPage()
                y_position = height - 50

        c.save()

def download_resume(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'resumes', file_name)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf', as_attachment=True)
    else:
        return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
    

# class JobMatchingView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         try:
#             resume = Resume.objects.get(user=user, is_latest=True)
#         except Resume.DoesNotExist:
#             return Response({"error": "No resume found for the user."}, status=status.HTTP_404_NOT_FOUND)

#         resume_content = resume.content
#         matched_jobs = match_jobs(resume_content)
#         return Response(matched_jobs, status=status.HTTP_200_OK)

#     def post(self, request):
#         return self.get(request)


# class JobMatchingView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         print(f"User {user.id} is requesting job matching.")

#         try:
#             # Attempt to fetch the latest resume for the user
#             resume = Resume.objects.get(user=user, is_latest=True)
#             print(f"Found latest resume for user {user.id}.")
#         except Resume.DoesNotExist:
#             # If no resume is found for the user
#             print(f"Error: No resume found for user {user.id}.")
#             return Response({"error": "No resume found for the user."}, status=status.HTTP_404_NOT_FOUND)

#         # If resume is found, log the resume content retrieval
#         resume_content = resume.content
#         print(f"Resume content retrieved for user {user.id}, proceeding to match jobs.")

#         # Perform the job matching
#         matched_jobs = match_jobs(resume_content)
#         print(f"Job matching completed for user {user.id}, {len(matched_jobs)} jobs found.")

#         # Return the matched jobs
#         return Response(matched_jobs, status=status.HTTP_200_OK)

#     def post(self, request):
#         print("POST request received, forwarding to GET method.")
#         return self.get(request)

# from django.http import JsonResponse
# from resume.services.companies import match_jobs_with_resume
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def JobMatchingView(request):
#     if request.method == "POST":
#         resume_content = request.POST.get("resume_content", "")
#         if not resume_content:
#             return JsonResponse({"error": "Resume content is required"}, status=400)

#         matched_jobs = match_jobs_with_resume(resume_content)
#         return JsonResponse({"matched_jobs": matched_jobs}, status=200)

#     return JsonResponse({"error": "Invalid request method"}, status=405)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from resume.services.companies import match_jobs_with_resume
from resume.models import Resume

from resume.services.pdf_processor import extract_resume_from_pdf
@csrf_exempt
def modify_resume(request):
    """
    Endpoint to modify resume based on job description.
    """
    if request.method == 'POST':
        try:
            resume_file = request.FILES['resume']  # Resume file uploaded by user
            job_description = request.POST['job_description']

            # Extract resume content from PDF
            resume_content = extract_resume_from_pdf(resume_file)

            # Rewrite resume according to job description
            original_resume = {
                'summary': 'Extracted Summary',
                'skills': 'Extracted Skills',
                'experience': 'Extracted Experience',
                'education': 'Extracted Education',
                'projects': 'Extracted Projects'
            }
            rewritten_resume = rewrite_resume(original_resume, job_description)

            return JsonResponse({'rewritten_resume': rewritten_resume})

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)

@csrf_exempt
def match_jobs_view(request):
    """
    Endpoint to match jobs based on resume content.
    """
    if request.method == 'POST':
        try:
            resume_file = request.FILES['resume']  # Resume file uploaded by user

            # Extract resume content from PDF
            resume_content = extract_resume_from_pdf(resume_file)

            # Match jobs with the extracted resume content
            matched_jobs = match_jobs(resume_content)

            return JsonResponse({'matched_jobs': matched_jobs})

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {str(e)}"}, status=500)