# resume_parser.py
import re
import spacy
from pdfminer.high_level import extract_text

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# Skill list – customize as needed
skill_list = [
    'python', 'java', 'sql', 'excel', 'c++', 'html', 'css', 'javascript',
    'pandas', 'numpy', 'django', 'flask', 'git', 'linux', 'machine learning'
]

def extract_text_from_pdf(file_path):
    return extract_text(file_path)

def extract_email(text):
    match = re.findall(r'\S+@\S+', text)
    return match[0] if match else None

def extract_phone(text):
    match = re.findall(r'\+?\d[\d -]{8,12}\d', text)
    return match[0] if match else None

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    return None

def extract_skills(text):
    text = text.lower()
    found_skills = [skill for skill in skill_list if skill in text]
    return list(set(found_skills))

def parse_resume(file_path):
    text = extract_text_from_pdf(file_path)

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "no_of_pages": text.count("Page") if "Page" in text else 1,
        "raw_text": text
    }
