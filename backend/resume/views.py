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
# from resume.services.job_matching import match_jobs
# from resume.services.companies import Companies


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


# class ResumeRewriteView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request, *args, **kwargs):
#         user = request.user

#         # Fetch the user's latest resume
#         try:
#             resume = Resume.objects.get(user=user, is_latest=True)
#         except Resume.DoesNotExist:
#             return Response(
#                 {"error": "No latest resume found for the user."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         # Get the job description from the request
#         job_description = request.data.get("job_description")
#         if not job_description:
#             return Response(
#                 {"error": "Job description is required."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Extract text content from the resume
#         file_content = None
#         if resume.file.name.endswith(".pdf"):
#             file_content = extract_text_from_pdf(resume.file.path)
#         else:
#             try:
#                 file_content = resume.file.read().decode("utf-8", errors="replace")
#             except Exception as e:
#                 return Response(
#                     {"error": f"Failed to read resume file: {str(e)}"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#         if not file_content:
#             return Response(
#                 {"error": "Failed to extract text from the resume."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # Call the resume rewriting service
#         rewritten_resume = rewrite_resume(file_content, job_description)

#         if not rewritten_resume:
#             return Response(
#                 {"error": "Failed to rewrite resume."},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

#         # Deduct one token for premium users
#         user_profile = UserProfile.objects.get(user=user)
#         if user_profile.user_type == "premium":
#             user_profile.premium_tokens -= 1
#             user_profile.save()

#         # Generate a new PDF with the rewritten resume
#         output_pdf_path = os.path.join(settings.MEDIA_ROOT, 'resumes', f"rewritten_resume_{resume.id}.pdf")
#         self.create_rewritten_pdf(output_pdf_path, rewritten_resume)

#         file_url = reverse('resume:download', kwargs={'file_name': f"rewritten_resume_{resume.id}.pdf"})

#         return Response({
#             "message": "Resume rewritten successfully",
#             "file_url": file_url
#         })

#     def create_rewritten_pdf(self, output_path, rewritten_resume):
#         c = canvas.Canvas(output_path, pagesize=letter)
#         width, height = letter

#         y_position = height - 50  # Start at the top of the page
#         for line in rewritten_resume.split("\n"):
#             if y_position < 50:  # Start a new page if near the bottom
#                 c.showPage()
#                 y_position = height - 50
#             c.drawString(50, y_position, line)
#             y_position -= 12  # Adjust line spacing

#         c.save()


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


# class JobMatchingView(APIView):
#     # permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         resume = Resume.objects.get(user=user, is_latest=True)
#         resume_content = extract_text_from_pdf(resume.file.path)
#         matched_jobs = match_jobs(resume_content)
#         return Response(matched_jobs, status=status.HTTP_200_OK)


# class JobMatchingView(APIView):
#     # permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user

#         # For testing, we use a sample resume content instead of extracting from a PDF
#         resume_content = """
#         Highly motivated and detail-oriented software engineer with experience in developing web applications, 
#         and a strong background in Python, Django, and React. Looking for opportunities to leverage expertise 
#         in full-stack development to contribute to innovative tech teams.
#         """

#         # Step 3: Initialize the Companies object to handle job scraping and matching
#         companies = Companies()

#         # Step 4: Match jobs with the resume content
#         matched_jobs = companies.match_jobs_with_resume(resume_content)

#         # Step 5: Handle possible errors from the job matching process
#         if "error" in matched_jobs:
#             return Response(matched_jobs, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # Step 6: Return the top matching jobs to the user
#         return Response(matched_jobs, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from resume.services.job_matching import match_jobs_with_resume


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
