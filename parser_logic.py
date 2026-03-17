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

def analyze_keyword_gap(resume_text, jd_text):
    # 1. Clean the Job Description text just like the resume
    clean_jd = clean_resume_text(jd_text).lower()
    resume_text_lower = resume_text.lower()

    # 2. Master list of Keywords (Skills, Tools, Technologies)
    # Expand this list to cover common tech stacks
    master_keywords = [
        "python", "java", "sql", "aws", "docker", "kubernetes", "git", 
        "machine learning", "artificial intelligence", "nlp", "scikit-learn", 
        "pandas", "numpy", "tensorflow", "pytorch", "flask", "django", 
        "react", "node", "html", "css", "javascript", "mongodb"
    ]

    # 3. Extract Years of Experience from JD (Regex pattern for "X+ years")
    experience_pattern = re.findall(r'(\d+)\+?\s*(?:years|yrs)', clean_jd)
    required_exp = experience_pattern[0] if experience_pattern else "Not Specified"

    # 4. Find Matched and Missing Keywords
    # Check what skills are mentioned in the JD
    skills_in_jd = [skill for skill in master_keywords if skill in clean_jd]
    
    # Check which of those JD skills are MISSING in the resume
    missing_skills = [skill for skill in skills_in_jd if skill not in resume_text_lower]
    matched_skills = [skill for skill in skills_in_jd if skill in resume_text_lower]

    return {
        "required_experience_level": required_exp,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_gap_count": len(missing_skills)
    }

# --- HOW TO TEST THIS NOW ---
sample_jd = "Looking for a Python developer with 3+ years experience in AWS and Docker."
resume_data = process_everything("ARSHIYA FIRDOUSE.pdf")
gap_results = analyze_keyword_gap(resume_data['cleaned_data'], sample_jd)
print(gap_results)
