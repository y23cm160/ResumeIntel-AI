import streamlit as st
import json
from parser_logic import process_everything, analyze_keyword_gap  # Member 2
from ai_logic import get_ai_analysis                          # Member 1

# 1. Page Configuration
st.set_page_config(page_title="AI Resume Mentor | DeployIt 2026", layout="wide")

# 2. Header Section
st.title("🚀 AI Resume Analyser & Career Mentor")
st.markdown("### Get ATS scores, skill gaps, and career insights instantly.")
st.markdown("---")

# 3. Sidebar for Inputs
with st.sidebar:
    st.header("Step 1: Data Input")
    resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    jd_text = st.text_area("Target Job Description", height=250, placeholder="Paste the JD here...")
    
    # The Trigger Button
    analyze_btn = st.button("🔍 Analyze & Rewrite")

# 4. Processing Logic
if analyze_btn:
    if resume_file and jd_text.strip():
        with st.spinner("🤖 AI is analyzing your profile..."):
            try:
                # --- CALLING MEMBER 2 (Parser) ---
                data = process_everything(resume_file)
                gap_results = analyze_keyword_gap(data["cleaned_data"], jd_text)
                
                missing_str = ", ".join(gap_results["missing_skills"]) if gap_results["missing_skills"] else "None"
                matched_str = ", ".join(gap_results["matched_skills"]) if gap_results["matched_skills"] else "None"

                # --- CALLING MEMBER 1 (AI Logic) ---
                ai_results = get_ai_analysis(
                    data["cleaned_data"], 
                    jd_text, 
                    missing_str
                )

                # 5. Main Results Dashboard
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.subheader("🎯 Fit Score")
                    score = ai_results.get("score", 0)
                    delta_msg = "Excellent" if score > 80 else "Needs Improvement"
                    st.metric(label="ATS Compatibility", value=f"{score}%", delta=delta_msg)
                    
                    st.write(f"📧 **Email:** {data['email']}")
                    st.write(f"📱 **Phone:** {data['phone']}")
                    st.write(f"📅 **Exp Required:** {gap_results['required_experience_level']}")
                   
                with col2:
                    st.subheader("💡 AI Career Reasoning")
                    st.info(ai_results.get("justification", "Analysis complete."))
                    st.success(f"**Pro Tip:** {ai_results.get('career_advice', 'Keep building!')}")

                st.markdown("---")

                # 6. ATS Keyword Gap Analysis
                st.subheader("📊 ATS Keyword Gap Analysis")
                present, missing = st.columns(2)
                with present:
                    st.success(f"**Skills Found:**\n{matched_str}")
                with missing:
                    st.error(f"**Missing Keywords:**\n{missing_str}")

                st.markdown("---")

                # 7. AI-Rewritten Suggestions
                st.subheader("📝 AI-Rewritten Suggestions")
                st.caption("Focusing on impact-driven metrics rather than just tasks.")
                
                # Format the Rewrites for a clean table
                rewrites = ai_results.get("rewrites", [])
                if rewrites:
                    # Creating a list of dicts for the table
                    table_data = [{"Before (Task)": item["Before"], "After (Impact)": item["After"]} for item in rewrites]
                    st.table(table_data)
                else:
                    st.write("No specific rewrites suggested.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("⚠️ Please upload a PDF resume and paste a Job Description to begin.")

# 8. Footer
st.markdown("---")
st.caption("DeployIt 2026 | Team: AI Resume Mentor")
