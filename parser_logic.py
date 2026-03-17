import pdfplumber
import re

# 1. THE ENGINE: Extracts raw text from the PDF
def get_text_from_any_file(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            full_text = [page.extract_text() for page in pdf.pages if page.extract_text()]
            return "\n".join(full_text)
    except Exception as e:
        return f"Error reading PDF: {e}"

# 2. THE FILTER: Cleans the text so the AI isn't confused
def clean_resume_text(raw_text):
    # Remove weird non-English symbols
    text = raw_text.encode("ascii", "ignore").decode()
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# 3. THE ANALYSER: Pulls out specific contact info
def extract_contact(text):
    # Improved email regex
    email = re.findall(r'[a-zA-Z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', text)

    # Improved phone regex: Handles +91, 91, or just 10 digits
    # This looks for a '+' (optional), then 10 to 12 digits in a row
    phone = re.findall(r'\+?\d{10,12}', text)

    return {
        "email": email[0] if email else "Not Found",
        "phone": phone[0] if phone else "Not Found"
    }

# 4. THE HAND-OFF: This is what you give your teammates
def process_everything(uploaded_file):
    raw = get_text_from_any_file(uploaded_file)
    clean = clean_resume_text(raw)
    contact = extract_contact(clean)

    return {
        "cleaned_data": clean,
        "email": contact["email"],
        "phone": contact["phone"]
    }

import pdfplumber
import re

# (Keep functions 1, 2, 3, and 4 exactly as you have them)

def analyze_keyword_gap(resume_text, jd_text):
    # 1. Clean the Job Description text just like the resume
    clean_jd = clean_resume_text(jd_text).lower()
    resume_text_lower = resume_text.lower()

    # 2. Master list of Keywords (Skills, Tools, Technologies)
    master_keywords = [
        "python", "java", "sql", "aws", "docker", "kubernetes", "git", 
        "machine learning", "artificial intelligence", "nlp", "scikit-learn", 
        "pandas", "numpy", "tensorflow", "pytorch", "flask", "django", 
        "react", "node", "html", "css", "javascript", "mongodb"
    ]

    # 3. EDUCATION/QUALIFICATION CHECK (New Addition)
    # List of common degrees to look for in the JD and Resume
    degree_hierarchy = ["phd", "master", "m.tech", "msc", "b.tech", "b.e", "bsc", "bachelor"]
    
    required_degree = "Not Specified"
    for degree in degree_hierarchy:
        if degree in clean_jd:
            required_degree = degree
            break
            
    # Check if the candidate has the required degree (or higher)
    has_required_education = False
    if required_degree == "Not Specified":
        has_required_education = True
    else:
        # Simple check: Does the degree keyword appear in the resume?
        if required_degree in resume_text_lower:
            has_required_education = True

    # 4. Extract Years of Experience from JD
    experience_pattern = re.findall(r'(\d+)\+?\s*(?:years|yrs)', clean_jd)
    required_exp = experience_pattern[0] if experience_pattern else "Not Specified"

    # 5. Find Matched and Missing Keywords
    skills_in_jd = [skill for skill in master_keywords if skill in clean_jd]
    missing_skills = [skill for skill in skills_in_jd if skill not in resume_text_lower]
    matched_skills = [skill for skill in skills_in_jd if skill in resume_text_lower]

    return {
        "required_experience_level": required_exp,
        "required_education": required_degree,
        "education_match": "Yes" if has_required_education else "No",
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_gap_count": len(missing_skills)
    }

# --- TEST IT ---
sample_jd = "Looking for a Python developer with a B.Tech and 3+ years experience in AWS."
# Use your resume data
resume_data = process_everything("ARSHIYA FIRDOUSE.pdf") 
gap_results = analyze_keyword_gap(resume_data['cleaned_data'], sample_jd)
print(gap_results)
