import re
import spacy
from pdfminer.high_level import extract_text
from datetime import datetime


# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# General skill list – add as needed
skill_list = [
    'python', 'java', 'sql', 'excel', 'c', 'c++', 'html', 'css', 'javascript',
    'pandas', 'numpy', 'django', 'flask', 'git', 'linux', 'machine learning',
    'mongodb', 'mysql', 'postgresql', 'oracle', 'sqlite'
]

# Database specific keywords
db_keywords = ["mysql", "mongodb", "postgresql", "oracle", "sqlite", "sql server"]

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


from datetime import datetime
import re

def extract_workexp(text):
    text_lower = text.lower()

    # Common section headers for experience
    experience_sections = [
        "experience", "work experience", "professional experience",
        "employment history", "work history", "career", "internship", "internships",
        "projects", "job", "jobs"
    ]

    # Try to capture text blocks after these headers
    search_texts = []
    for kw in experience_sections:
        pattern = rf"{kw}[\s\S]{{0,1500}}"   # capture up to 1500 chars after keyword
        matches = re.findall(pattern, text_lower)
        search_texts.extend(matches)

    # If no experience section found, fallback to full text
    if not search_texts:
        search_texts = [text_lower]

    # Date formats: Jan 2020 – Dec 2021, September 2020 - Present, 2020-2022
    date_pattern = r'([A-Za-z]{3,9}|\d{4})\.?\s*(\d{4})?\s*[–-]\s*([A-Za-z]{3,9}|Present|Current|Ongoing|\d{4})\.?\s*(\d{4})?'

    total_months = 0
    print("\n=== Experience Ranges Detected ===")

    for block in search_texts:
        matches = re.findall(date_pattern, block, flags=re.IGNORECASE)

        for start_month, start_year, end_month, end_year in matches:
            try:
                # Handle year-only case (e.g., 2020-2022)
                if start_month.isdigit() and not start_year:
                    start_date = datetime(int(start_month), 1, 1)
                else:
                    # Try short month name
                    try:
                        start_date = datetime.strptime(f"{start_month} {start_year}", "%b %Y")
                    except:
                        # Try full month name
                        try:
                            start_date = datetime.strptime(f"{start_month} {start_year}", "%B %Y")
                        except:
                            continue

                # Parse end date
                if end_month.lower().startswith(("present", "current", "ongoing")):
                    end_date = datetime.now()
                elif end_month.isdigit() and not end_year:  # Year-only end
                    end_date = datetime(int(end_month), 12, 1)
                else:
                    year = end_year.strip() if end_year else start_year
                    try:
                        end_date = datetime.strptime(f"{end_month} {year}", "%b %Y")
                    except:
                        try:
                            end_date = datetime.strptime(f"{end_month} {year}", "%B %Y")
                        except:
                            continue

                # Calculate months
                diff_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
                if diff_months < 0:  # bad parsing
                    continue

                total_months += diff_months
                print(f"{start_date.strftime('%b %Y')} – {end_date.strftime('%b %Y')}: {diff_months} months")

            except Exception as e:
                continue

    print("=================================\n")

    return round(total_months / 12, 1) if total_months > 0 else 0









db_keywords = ["mysql","sql", "mongodb", "postgresql", "oracle", "sqlite", "sql server"]

def extract_num_db_skills(text):
    text = text.lower()
    found_dbs = [db for db in db_keywords if db in text]
    return len(found_dbs), found_dbs


def parse_resume(file_path):
    text = extract_text_from_pdf(file_path)

    workexp = extract_workexp(text)
    yearscodepro = workexp  # assumption
    noofdbknown, db_names = extract_num_db_skills(text)

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "WorkExp": workexp,
        "YearsCodePro": yearscodepro,
        "NumberOfDatabasesKnown": noofdbknown,
        "DatabaseSkills": db_names,   # NEW: list of DBs
        "no_of_pages": text.count("Page") if "Page" in text else 1,
        "raw_text": text
    }

