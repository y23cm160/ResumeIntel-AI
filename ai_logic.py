import google.generativeai as genai
import json
import os
import warnings
from dotenv import load_dotenv

# 1. Hide the annoying warnings for the demo
warnings.filterwarnings("ignore", category=FutureWarning)

# 2. Load the API Key
load_dotenv()

def get_ai_analysis(resume_text, jd_text, missing_keywords):
    """
    Member 1's Brain: Takes inputs from Member 2/4 and returns a JSON report.
    """
    # Configure API
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"score": 0, "justification": "API Key Missing in .env file", "career_advice": "", "rewrites": []}
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # The Logic Instructions
    prompt = f"""
    You are a Senior Recruiter. Analyze this candidate:
    RESUME: {resume_text}
    JD: {jd_text}
    MISSING SKILLS: {missing_keywords}

    Return ONLY a JSON object with:
    1. "score": integer 0-100
    2. "justification": 2 sentences
    3. "career_advice": 1 tip
    4. "rewrites": list of 3 dicts with keys "Before" and "After"
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        return {
            "score": 0,
            "justification": f"AI Error: {str(e)}",
            "career_advice": "Check internet/API key.",
            "rewrites": []
        }
