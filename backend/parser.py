import pdfplumber
import fitz  # PyMuPDF
import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)           # collapse multiple spaces
    text = re.sub(r'[^\x00-\x7F]+', ' ', text) # remove non-ASCII characters
    return text.strip()

def extract_from_pdf(file_path):
    text = ""
    try:
        # Primary method: pdfplumber (better for text-heavy PDFs)
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        pass

    # Fallback: PyMuPDF (better for styled/graphical resumes)
    if len(text.strip()) < 100:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()

    return clean_text(text)

def extract_text(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        return extract_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        from docx import Document
        doc = Document(file_path)
        text = "\n".join(p.text for p in doc.paragraphs)
        return clean_text(text)
    else:
        raise ValueError("Only PDF and DOCX files are supported.")