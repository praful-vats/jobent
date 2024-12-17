from django.contrib.auth.models import User
from django.db import models
import PyPDF2 # type: ignore

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow null users
    file = models.FileField(upload_to='resumes/')
    file_name = models.CharField(max_length=255, blank=True)
    content = models.TextField(default='')  # Provide a default value for content
    is_latest = models.BooleanField(default=False)
    job_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the file first
        if self.file:
            self.file_name = self.file.name
            self.content = self.extract_text_from_file()
        super().save(*args, **kwargs)  # Save again to update the content

    def extract_text_from_file(self):
        # Extract text content from the file
        if self.file.name.endswith(".pdf"):
            return self.extract_text_from_pdf(self.file.path)
        else:
            try:
                return self.file.read().decode("utf-8", errors="replace")
            except Exception as e:
                return ""

    def extract_text_from_pdf(self, pdf_file_path):
        with open(pdf_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"