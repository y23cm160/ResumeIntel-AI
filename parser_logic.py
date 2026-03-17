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
