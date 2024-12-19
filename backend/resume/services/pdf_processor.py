import fitz  # PyMuPDF

def extract_resume_from_pdf(pdf_path):
    """
    Extract text from a PDF resume.
    """
    document = fitz.open(pdf_path)
    resume_text = ""
    for page in document:
        resume_text += page.get_text("text")  # Extract text from each page
    return resume_text
