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
from io import BytesIO
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.pdfgen import canvas # type: ignore
import PyPDF2 # type: ignore

def extract_text_from_pdf(pdf_file_path):
    """
    Extract text content from a PDF file.
    """
    with open(pdf_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text


class ResumeUploadView(ListCreateAPIView):
    """
    View to upload and list resumes.
    """
    permission_classes = [IsAuthenticated]
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def perform_create(self, serializer):
        user = self.request.user
        # Set the latest uploaded resume to "is_latest=True" and others to False
        Resume.objects.filter(user=user).update(is_latest=False)
        serializer.save(user=user, is_latest=True)


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

        # Check if the user is premium and has sufficient tokens
        if profile.user_type == "premium" and profile.premium_tokens <= 0:
            return Response(
                {"error": "No premium tokens available."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Fetch the resume instance
        try:
            resume = Resume.objects.get(pk=kwargs["pk"], user=user)
        except Resume.DoesNotExist:
            return Response(
                {"error": "Resume not found."}, status=status.HTTP_404_NOT_FOUND
            )

        job_description = request.data.get("job_description")

        if not job_description:
            return Response(
                {"error": "Job description is required."}, status=status.HTTP_400_BAD_REQUEST
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

        # Return the rewritten resume content
        return Response({"rewritten_resume": rewritten_resume}, status=status.HTTP_200_OK)