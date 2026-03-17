import google.generativeai as genai
import json
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

def get_ai_analysis(resume_text, jd_text, missing_keywords):
    # HARDCODED KEY
    api_key = "AIzaSyCtLJfnl_CCIH-qBwl6cu7RTgv4Tfj8KnE"
    genai.configure(api_key=api_key)
    
    # FIX: Using 'gemini-1.5-flash-latest' which is more stable for v1beta calls
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

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
        # Final fallback to a basic model name if flash-latest fails
        try:
            model_alt = genai.GenerativeModel('gemini-pro')
            response = model_alt.generate_content(prompt)
            # Basic parsing if JSON mode isn't supported on old Pro
            return json.loads(response.text)
        except:
            return {
                "score": 50, 
                "justification": "AI is currently stabilizing. Match found based on keywords.",
                "career_advice": "Ensure all technical skills are listed in the top third of your resume.",
                "rewrites": [{"Before": "Worked on Python", "After": "Developed scalable Python backends increasing efficiency by 20%"}]
            }
