import streamlit as st
from openai import OpenAI
import os
import pdfplumber
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Job Screener", page_icon="📄")
st.title("AI Job Application Screener")
st.write("Paste a job description and upload or paste your resume to get a match score and feedback.")

job_description = st.text_area("Job Description", height=200, placeholder="Paste the job posting here...")

st.subheader("Your Resume")
uploaded_file = st.file_uploader("Upload your resume as a PDF", type="pdf")
resume_text = st.text_area("Or paste your resume text here", height=200, placeholder="Paste your resume text here...")

resume = ""
if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            resume += page.extract_text() or ""
    st.success("PDF uploaded and extracted successfully.")
elif resume_text:
    resume = resume_text

if st.button("Analyze"):
    if not job_description or not resume:
        st.warning("Please fill in the job description and provide your resume.")
    else:
        with st.spinner("Analyzing..."):
            prompt = f"""
You are an expert resume reviewer and hiring manager.

Given the job description and resume below, provide:
1. A match score from 0 to 100 (how well the resume fits the job)
2. A list of key skills or qualifications from the job that are MISSING from the resume
3. Specific, actionable suggestions to improve the resume for this role

Format your response exactly like this:
**Match Score:** [score]/100

**Missing Skills/Qualifications:**
- [item]
- [item]

**Suggestions to Improve Your Resume:**
- [suggestion]
- [suggestion]

---

Job Description:
{job_description}

Resume:
{resume}
"""
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content
            st.markdown(result)
