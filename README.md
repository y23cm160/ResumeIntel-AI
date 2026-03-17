Project Overview
Most students face rejection because their resumes fail to pass Applicant Tracking Systems (ATS) due to formatting issues, missing keywords, or weak action verbs.

AI Resume Mentor is an AI-powered platform that analyzes resumes from a recruiter’s perspective and provides:
-Structured feedback
-ATS gap analysis
-Impact-driven rewrites
Unlike standard rule-based checkers, this system uses LLM reasoning to evaluate career narrative coherence and role fit holistically.
Key Features
🔍 Structured AI Critique
Deep analysis across multiple professional dimensions
Evaluates clarity, impact, and role alignment

📊 ATS Keyword Gap Analysis
Compares resume with job description
Identifies missing critical skills and keywords

✍️ Impact-Driven Rewrites
Generates improved bullet points
Provides clear Before & After comparison

📈 Holistic Scoring
Overall resume score
-Supported with simple, human-readable justification

Clean Results Dashboard
-User-friendly UI
-Designed for clarity and easy scanning
🛠️ Technical Stack

LLM Engine: Gemini 1.5 Flash (Google Generative AI API)
Frontend UI: Gradio
PDF Processing: pdfplumber
Data Structuring: JSON mode

🏗️ System Architecture
The system follows a modular design:

📂 Parser (parser_logic.py)
Extracts text from PDF resumes
Cleans non-ASCII characters
Uses Regex for:
Contact details
Experience level detection

🧠 AI Engine (ai_logic.py)
Uses engineered prompts
Focuses on:
Language quality
Career narrative
Role alignment
Avoids simple keyword-based evaluation

🔗 Integrator (app.py)
Connects parser and AI engine
Handles data flow
Renders results in Gradio dashboard

⚙️ Getting Started
✅ Prerequisites

Python 3.8+
Google Gemini API Key

📥 Installation
Clone the repository:
git clone https://github.com/your-username/ai-resume-mentor.git
cd ai-resume-mentor

Install dependencies:
pip install gradio google-generativeai pdfplumber
▶️ Run the Application
python app.py


