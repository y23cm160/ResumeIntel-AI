# 📄 AI Resume Mentor: ATS Analysis & Intelligent Resume Enhancement

## 🔍 Overview

This project presents an **AI-powered resume analysis platform** that evaluates resumes from a recruiter’s perspective.

It identifies **ATS-related issues**, missing keywords, and weak action verbs while providing **impact-driven rewrites** and structured feedback.

The goal is to **improve resume quality, ATS compatibility, and role alignment**, not just keyword matching.

---

## 📁 Input Data

The system works with:

* **📄 Resume (PDF)** – Uploaded by the user
* **📌 Job Description (Optional)** – Used for ATS comparison

Extracted information includes:

* Contact details
* Skills
* Experience
* Resume content structure

---

## 🧠 Methodology

* Resume text extraction using PDF parsing
* Cleaning and normalization of raw text
* Prompt-engineered LLM analysis for:

  * Language quality
  * Career narrative coherence
  * Role fit

Core evaluation logic:

```
Resume Score = f(Content Quality, ATS Match, Impact Strength, Role Alignment)
```

---

## 🔍 Model Analysis

The system performs multi-dimensional evaluation:

* **📊 Structured AI Critique**
  Analyzes clarity, tone, and professional impact

* **📌 ATS Keyword Gap Analysis**
  Compares resume against job description to detect missing skills

* **✍️ Impact Evaluation**
  Identifies weak bullet points and suggests stronger alternatives

* **📈 Holistic Scoring**
  Generates an overall score with explanation

---

## 📌 Results

* ✅ Improved resume clarity and professional tone
* 📈 Better alignment with job requirements
* 🔍 Identification of missing ATS keywords
* ✍️ Stronger, action-oriented bullet points

⚠️ Results depend on input quality and LLM interpretation.

---

## ⚠️ Limitations

* Dependent on LLM output quality
* No guarantee of ATS success across all platforms
* Limited domain-specific customization
* PDF parsing may fail for complex formats

---

## 🔮 Future Work

* Multi-resume comparison
* Resume template generation
* Real-time ATS scoring visualization
* Integration with job portals
* Domain-specific optimization (Tech, Finance, etc.)

---

## 🛠️ Tools Used

* Python
* Gradio
* Google Generative AI (Gemini 1.5 Flash)
* pdfplumber
* JSON

---

## 🧾 Final Note

This project goes beyond rule-based systems by leveraging **LLM reasoning** to evaluate resumes holistically.

It demonstrates a strong understanding of **AI-driven text analysis, ATS optimization, and real-world application design**.

---

