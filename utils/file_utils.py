import PyPDF2
import io
import streamlit as st

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

def validate_file_size(file, max_size_mb=10):
    """Validate uploaded file size"""
    if file is not None:
        file_size = len(file.getvalue()) / (1024 * 1024)  # Convert to MB
        if file_size > max_size_mb:
            st.error(f"File size ({file_size:.1f} MB) exceeds maximum allowed size ({max_size_mb} MB)")
            return False
    return True

def get_cv_text(uploaded_file, text_input):
    """Extract CV text from either uploaded file or text input"""
    cv_text = ""
    
    if uploaded_file and validate_file_size(uploaded_file):
        cv_text = extract_text_from_pdf(uploaded_file)
    elif text_input.strip():
        cv_text = text_input.strip()
    
    return cv_text
