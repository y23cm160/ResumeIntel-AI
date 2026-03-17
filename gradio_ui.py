import gradio as gr
import pdfplumber
import re

# -------------------- BACKEND (SAME AS YOURS) --------------------
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

    degree_hierarchy = ["phd", "master", "m.tech", "msc", "b.tech", "b.e", "bsc", "bachelor"]
    required_degree = "Not Specified"

    for degree in degree_hierarchy:
        if degree in clean_jd:
            required_degree = degree
            break

    has_required_education = required_degree in resume_text_lower if required_degree != "Not Specified" else True

    experience_pattern = re.findall(r'(\d+)\+?\s*(?:years|yrs)', clean_jd)
    required_exp = experience_pattern[0] if experience_pattern else "Not Specified"

    skills_in_jd = [skill for skill in master_keywords if skill in clean_jd]
    missing_skills = [skill for skill in skills_in_jd if skill not in resume_text_lower]
    matched_skills = [skill for skill in skills_in_jd if skill in resume_text_lower]

    return required_exp, required_degree, "Yes" if has_required_education else "No", matched_skills, missing_skills


# -------------------- UI LOGIC --------------------
def analyze_resume_ui(resume_file, jd_text):
    if resume_file is None or jd_text.strip() == "":
        return 0, "", "", "", "", "", "", ""

    data = process_everything(resume_file)
    exp, degree, edu_match, matched, missing = analyze_keyword_gap(data["cleaned_data"], jd_text)

    total = len(matched) + len(missing)
    score = int((len(matched) / total) * 100) if total > 0 else 0

    matched = ", ".join(matched) if matched else "None"
    missing = ", ".join(missing) if missing else "None"

    return score, data["email"], data["phone"], matched, missing, exp, degree, edu_match


# -------------------- ADVANCED CSS --------------------
custom_css = """
body {
    background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1f4037);
    background-size: 400% 400%;
    animation: gradientMove 10s ease infinite;
}

@keyframes gradientMove {
    0% {background-position: 0%}
    50% {background-position: 100%}
    100% {background-position: 0%}
}

::-webkit-scrollbar {
    display: none;
}

.card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 0 20px rgba(0,0,0,0.4);
}

button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    border-radius: 12px;
    font-size: 18px;
    transition: 0.3s;
    box-shadow: 0 0 15px rgba(0,114,255,0.5);
}

button:hover {
    transform: scale(1.07);
    box-shadow: 0 0 25px rgba(0,114,255,0.9);
}

input, textarea {
    border-radius: 10px !important;
}
"""

# -------------------- UI --------------------
with gr.Blocks(css=custom_css) as demo:

    gr.Markdown("""
    # 🌟 Smart ATS Analyzer  
    ### 💼 AI Resume Intelligence Dashboard
    """)

    with gr.Row():
        resume = gr.File(label="📂 Upload Resume", elem_classes="card")
        jd = gr.Textbox(label="📌 Job Description", lines=8, elem_classes="card")

    analyze_btn = gr.Button("🚀 Analyze Resume")

    gr.Markdown("## 📊 Results")

    score = gr.Slider(0, 100, label="Match Score (%)")

    with gr.Row():
        email = gr.Textbox(label="📧 Email")
        phone = gr.Textbox(label="📱 Phone")

    matched = gr.Textbox(label="✅ Matched Skills")
    missing = gr.Textbox(label="❌ Missing Skills")

    with gr.Row():
        exp = gr.Textbox(label="📅 Experience")
        degree = gr.Textbox(label="🎓 Degree")
        edu_match = gr.Textbox(label="✔ Education Match")

    analyze_btn.click(
        analyze_resume_ui,
        inputs=[resume, jd],
        outputs=[score, email, phone, matched, missing, exp, degree, edu_match]
    )

demo.launch()
