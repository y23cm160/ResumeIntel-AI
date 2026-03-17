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
if analyze_btn:
    if resume_file and jd_text:
        with st.spinner("Pipeline Active: Parsing and Analyzing..."):
            
            # --- STEP 1: Execute Member 2's Parser ---
            # Using the 'process_everything' function Member 2 provided
            from parser_logic import process_everything
            parser_results = process_everything(resume_file)
            resume_text = parser_results["cleaned_data"]
            
            # Display Contact Info in the sidebar or a small box (Member 3 UI touch)
            st.sidebar.success(f"Extracted: {parser_results['email']}")

            # --- STEP 2: Execute Member 1's AI Brain ---
            # Passing the cleaned text to Member 1's AI logic
            analysis = get_ai_analysis(resume_text, jd_text)
            
            # --- STEP 3: Display Results (Dynamic Data) ---
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("🎯 Fit Score")
                # Use the 'score' key from Member 1's JSON
                st.metric(label="ATS Compatibility", value=f"{analysis['score']}%")
                
            with col2:
                st.subheader("🧠 AI Career Reasoning")
                # Use the 'justification' key from Member 1's JSON
                st.write(f"**Justification:** {analysis['justification']}")

            st.markdown("---")

            # 5. ATS Keyword Gap Analysis (Dynamic)
            st.subheader("🔍 ATS Keyword Gap Analysis")
            present, missing = st.columns(2)
            with present:
                # Use 'found_keywords' from Member 1
                st.success(f"**Skills Found:** {', '.join(analysis['found_keywords'])}")
            with missing:
                # Use 'missing_keywords' from Member 1
                st.error(f"**Missing Keywords:** {', '.join(analysis['missing_keywords'])}")

            st.markdown("---")

            # 6. AI-Rewritten Bullets (Dynamic Table)
            st.subheader("✍️ AI-Rewritten Suggestions")
            st.info("AI Core Constraint: Evaluating career narrative coherence.")
            
            # Pass the 'rewrites' list from Member 1 directly into the table
            st.table(analysis['rewrites'])

    else:
        st.warning("Please upload a PDF resume and paste a Job Description to begin.")
        
st.markdown("---")
st.caption("DeployIt 2026 | Team: AI Resume Mentor")
