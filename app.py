import streamlit as st
from parser_logic import extract_text_from_pdf  # Member 2's code
from ai_logic import get_ai_analysis          # Member 1's code

# 1. Page Configuration (Judged Criterion: UI Design)
st.set_page_config(page_title="AI Resume Mentor | DeployIt 2026", layout="wide")

# 2. Header Section
st.title(" AI Resume Analyser & Career Mentor")
st.markdown("---")

# 3. Sidebar for Inputs (Expected Outcome: Resume Upload & JD)
with st.sidebar:
    st.header("Step 1: Data Input")
    resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
    jd_text = st.text_area("Target Job Description", height=200, placeholder="Paste the JD here...")
    
    # The Trigger Button
    analyze_btn = st.button("🚀 Analyze & Rewrite")

# 4. Main Results Dashboard (Expected Outcome: Clean Results Dashboard)
# 4. Main Results Dashboard (Data Pipeline Integration)
# 4. Main Results Dashboard (Final Integrated Pipeline)
if analyze_btn:
    if resume_file and jd_text:
        with st.spinner("AI is reasoning about your career narrative..."):
            try:
                # --- STEP 1: Member 2's Parser ---
                from parser_logic import process_everything
                parser_results = process_everything(resume_file)
                resume_text = parser_results["cleaned_data"]
                
                # Show contact info in sidebar (UI Polish)
                st.sidebar.success(f"📧 {parser_results['email']}")
                st.sidebar.info(f"📞 {parser_results['phone']}")

                # --- STEP 2: Member 1's AI Brain ---
                # We identify keywords from JD that aren't in the Resume 
                # to pass into her 'missing_keywords' parameter
                resume_words = set(resume_text.lower().split())
                jd_words = set(jd_text.lower().split())
                missing_list = list(jd_words - resume_words)[:5] # Top 5 differences

                # Calling her function with the 3 required arguments
                analysis = get_ai_analysis(resume_text, jd_text, missing_list)

                # --- STEP 3: Display Results (Matching Member 1's JSON Keys) ---
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.subheader("🎯 Fit Score")
                    st.metric(label="Match Quality", value=f"{analysis.get('score', 0)}%")
                    
                with col2:
                    st.subheader("🧠 Recruiter Justification")
                    st.write(analysis.get('justification', "No justification provided."))

                st.markdown("---")

                # Displaying her specific "career_advice" key
                st.subheader("💡 Career Tip")
                st.info(analysis.get('career_advice', "Keep improving!"))

                st.markdown("---")

                # Displaying her "rewrites" with capitalized "Before" and "After"
                st.subheader("✍️ AI-Rewritten Suggestions")
                if analysis.get('rewrites'):
                    st.table(analysis['rewrites'])
                else:
                    st.write("No rewrites generated.")

            except Exception as e:
                st.error(f"Integration Error: {e}")
    else:
        st.warning("Please upload a resume and paste a JD.")

            
            
