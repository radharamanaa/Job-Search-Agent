import io
import PyPDF2
import docx
import pandas as pd

def parse_resume(uploaded_file):
    """
    Parse uploaded resume file and extract text content.
    Supports PDF, DOCX, and TXT formats.
    
    Args:
        uploaded_file: The uploaded file object from Streamlit
        
    Returns:
        str: Extracted text from the resume
    """
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_type == 'pdf':
            return parse_pdf(uploaded_file)
        elif file_type == 'docx':
            return parse_docx(uploaded_file)
        elif file_type == 'txt':
            return parse_txt(uploaded_file)
        else:
            return "Unsupported file format. Please upload a PDF, DOCX, or TXT file."
    except Exception as e:
        return f"Error parsing resume: {str(e)}"

def parse_pdf(file):
    """Extract text from PDF file"""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def parse_docx(file):
    """Extract text from DOCX file"""
    doc = docx.Document(io.BytesIO(file.getvalue()))
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def parse_txt(file):
    """Extract text from TXT file"""
    return file.getvalue().decode("utf-8")