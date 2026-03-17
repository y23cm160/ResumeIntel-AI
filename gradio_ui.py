import gradio as gr
import pdfplumber
import re

# -------------------- MEMBER-2 CODE --------------------

def get_text_from_any_file(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            full_text = [page.extract_text() for page in pdf.pages if page.extract_text()]
            return "\n".join(full_text)
    except Exception as e:
        return f"Error reading PDF: {e}"

def clean_resume_text(raw_text):
    text = raw_text.encode("ascii", "ignore").decode()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_contact(text):
    email = re.findall(r'[a-zA-Z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', text)
    phone = re.findall(r'\+?\d{10,12}', text)

    return {
        "email": email[0] if email else "Not Found",
        "phone": phone[0] if phone else "Not Found"
    }

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
    clean_jd = clean_resume_text(jd_text).lower()
    resume_text_lower = resume_text.lower()

    master_keywords = [
        "python", "java", "sql", "aws", "docker", "kubernetes", "git",
        "machine learning", "artificial intelligence", "nlp", "scikit-learn",
        "pandas", "numpy", "tensorflow", "pytorch", "flask", "django",
        "react", "node", "html", "css", "javascript", "mongodb"
    ]

    experience_pattern = re.findall(r'(\d+)\+?\s*(?:years|yrs)', clean_jd)
    required_exp = experience_pattern[0] if experience_pattern else "Not Specified"

    skills_in_jd = [skill for skill in master_keywords if skill in clean_jd]
    missing_skills = [skill for skill in skills_in_jd if skill not in resume_text_lower]
    matched_skills = [skill for skill in skills_in_jd if skill in resume_text_lower]

    return {
        "required_experience_level": required_exp,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "total_gap_count": len(missing_skills)
    }

# -------------------- YOUR UI LOGIC --------------------

def analyze_resume_ui(resume_file, jd_text):
    if resume_file is None or jd_text.strip() == "":
        return 0, "Upload resume & enter JD", "", "", "", ""

    try:
        # Process resume
        data = process_everything(resume_file)

        # Analyze skills gap
        gap = analyze_keyword_gap(data["cleaned_data"], jd_text)

        total = len(gap["matched_skills"]) + len(gap["missing_skills"])
        score = int((len(gap["matched_skills"]) / total) * 100) if total > 0 else 0

        matched = ", ".join(gap["matched_skills"]) if gap["matched_skills"] else "None"
        missing = ", ".join([f"{s} (important skill)" for s in gap["missing_skills"]]) if gap["missing_skills"] else "None"

        return (
            score,
            data["email"],
            data["phone"],
            matched,
            missing,
            gap["required_experience_level"]
        )

    except Exception as e:
        return 0, f"Error: {e}", "", "", "", ""

# -------------------- UI DESIGN --------------------

with gr.Blocks() as demo:
    gr.Markdown("# 🚀 AI Resume Analyzer & Career Mentor")
    gr.Markdown("### Get ATS score, skill gaps & career insights instantly")

    with gr.Row():
        resume = gr.File(label="📂 Upload Resume (PDF)")
        jd = gr.Textbox(label="📌 Job Description", lines=5)

    analyze_btn = gr.Button("🚀 Analyze Resume")

    gr.Markdown("## 📊 Results Dashboard")

    score = gr.Slider(0, 100, label="Match Score (%)")

    with gr.Row():
        email = gr.Textbox(label="📧 Email")
        phone = gr.Textbox(label="📱 Phone")

    matched = gr.Textbox(label="✅ Matched Skills")
    missing = gr.Textbox(label="❌ Missing Skills")
    exp = gr.Textbox(label="📅 Required Experience")

    analyze_btn.click(
        analyze_resume_ui,
        inputs=[resume, jd],
        outputs=[score, email, phone, matched, missing, exp]
    )

demo.launch()
