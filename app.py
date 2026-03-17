import gradio as gr
from parser_logic import process_everything, analyze_keyword_gap  # Member 2's code
from ai_logic import get_ai_analysis                          # Member 1's code

# 1. The Bridge Function: This connects the UI to your Logic
def run_analysis(resume_file, jd_text):
    if resume_file is None or not jd_text.strip():
        return 0, "N/A", "N/A", "Please upload a file and enter JD", "N/A", "N/A", "N/A", "N/A", ""

    try:
        # --- EXECUTE PARSER (Member 2) ---
        data = process_everything(resume_file)
        gap = analyze_keyword_gap(data["cleaned_data"], jd_text)
        
        matched_str = ", ".join(gap["matched_skills"]) if gap["matched_skills"] else "None"
        missing_str = ", ".join(gap["missing_skills"]) if gap["missing_skills"] else "None"

        # --- EXECUTE AI LOGIC (Member 1) ---
        ai_results = get_ai_analysis(
            data["cleaned_data"], 
            jd_text, 
            missing_str
        )

        # Format Rewrites for display in a single Textbox
        rewrite_display = ""
        for item in ai_results.get("rewrites", []):
            rewrite_display += f"❌ BEFORE: {item['Before']}\n✅ AFTER: {item['After']}\n\n"

        # 2. Return the data in the EXACT order of the UI Outputs
        return (
            ai_results.get("score", 0),
            data["email"],
            data["phone"],
            matched_str,
            missing_str,
            gap["required_experience_level"],
            ai_results.get("justification", "No justification provided."),
            ai_results.get("career_advice", "No advice provided."),
            rewrite_display
        )

    except Exception as e:
        return 0, "Error", "Error", f"Runtime Error: {str(e)}", "", "", "", "", ""

# 3. UI Design using Gradio Blocks
with gr.Blocks(theme=gr.themes.Soft(), title="AI Resume Mentor") as demo:
    gr.Markdown("# 🚀 AI Resume Analyser & Career Mentor")
    gr.Markdown("### Upload your resume and job description to get AI-powered insights.")
    
    with gr.Row():
        with gr.Column(scale=1):
            resume_input = gr.File(label="📂 Upload Resume (PDF)")
            jd_input = gr.Textbox(label="📌 Job Description", lines=10, placeholder="Paste requirements here...")
            analyze_btn = gr.Button("🔍 Analyze & Rewrite", variant="primary")

        with gr.Column(scale=2):
            gr.Markdown("## 📊 Results Dashboard")
            score_out = gr.Slider(0, 100, label="ATS Match Score (%)")
            
            with gr.Row():
                email_out = gr.Textbox(label="📧 Email")
                phone_out = gr.Textbox(label="📱 Phone")
            
            with gr.Row():
                matched_out = gr.Textbox(label="✅ Matched Skills")
                missing_out = gr.Textbox(label="❌ Missing Skills")
            
            exp_out = gr.Textbox(label="📅 Required Experience")
            
            gr.Markdown("---")
            gr.Markdown("### 🧠 AI Insights")
            with gr.Row():
                justification_out = gr.Textbox(label="⚖️ Justification", lines=3)
                advice_out = gr.Textbox(label="💡 Career Advice")
            
            rewrites_out = gr.Textbox(label="📝 Resume Rewrites (Impact-Driven)", lines=8)

    # 4. THE CONNECTION (The "Handshake")
    # This maps the inputs to the function and the function's return values to the outputs
    analyze_btn.click(
        fn=run_analysis,
        inputs=[resume_input, jd_input],
        outputs=[
            score_out, email_out, phone_out, 
            matched_out, missing_out, exp_out, 
            justification_out, advice_out, rewrites_out
        ]
    )

# 5. Launch (Crucial for Colab)
if __name__ == "__main__":
    # share=True creates a public link for your team
    demo.launch(share=True, debug=True)
          
