import pdfplumber
import re

def extract_text_from_resume(file_path: str) -> str:
    """Extract all text from the uploaded resume PDF."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_skills(resume_text: str) -> list:
    """Extract simple skills from resume text using keyword matching."""
    skills_keywords = [
        "python", "java", "machine learning", "sql", "html", "css", "javascript",
        "flask", "django", "streamlit", "data analysis", "nlp", "deep learning"
    ]
    found_skills = [skill for skill in skills_keywords if skill.lower() in resume_text.lower()]
    return list(set(found_skills))
