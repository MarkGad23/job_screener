import streamlit as st
from openai import OpenAI
import os
import pdfplumber
from dotenv import load_dotenv
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Job Screener", page_icon="📄", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stMarkdown, .stTextArea, .stButton, p, div, span, label {
        font-family: 'Inter', sans-serif !important;
    }

    .block-container { padding-top: 0; max-width: 980px; }
    .stApp { background-color: #0c0e14; }

    /* ── Header ── */
    .app-header {
        display: flex;
        align-items: center;
        gap: 1.25rem;
        padding: 3rem 0 2.25rem 0;
        border-bottom: 1px solid #1a2236;
        margin-bottom: 3rem;
    }
    .app-header h1 {
        color: #dce3f0 !important;
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0 0 0.2rem 0;
        letter-spacing: -0.02em;
        font-family: 'Times New Roman', Times, serif !important;
    }
    .app-tagline {
        color: #8a9ec0;
        font-size: 1.05rem;
        margin: 0;
        font-weight: 400;
    }

    /* ── Field labels ── */
    .field-label {
        font-size: 1rem;
        font-weight: 500;
        color: #aab8d0;
        margin-bottom: 0.6rem;
        letter-spacing: 0.01em;
    }

    /* ── Text area ── */
    div[data-testid="stTextArea"] textarea {
        background: #10131d !important;
        border: 1px solid #1a2236 !important;
        border-radius: 8px;
        color: #e8edf8 !important;
        font-size: 1.05rem;
        line-height: 1.75;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 2px rgba(37,99,235,0.12) !important;
    }
    div[data-testid="stTextArea"] textarea::placeholder {
        color: #3d5070 !important;
    }

    /* ── File uploader — no box ── */
    div[data-testid="stFileUploader"] {
        background: transparent;
        border: none;
        padding: 0;
    }
    div[data-testid="stFileUploader"] * {
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        color: #8a9ec0 !important;
    }

    /* ── Button ── */
    .stButton > button {
        background: #2563eb !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.85rem 1rem;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.01em;
        transition: background 0.15s;
    }
    .stButton > button:hover { background: #1d4ed8 !important; }

    /* ── Results ── */
    .score-row {
        display: flex;
        align-items: baseline;
        gap: 0.75rem;
        margin-bottom: 0.6rem;
    }
    .score-num {
        font-size: 5.5rem;
        font-weight: 800;
        line-height: 1;
        letter-spacing: -0.05em;
        font-family: 'Inter', sans-serif !important;
    }
    .score-denom {
        font-size: 1.5rem;
        color: #5a7090;
        font-weight: 500;
    }
    .score-badge {
        font-size: 0.9rem;
        font-weight: 600;
        padding: 0.25rem 0.7rem;
        border-radius: 5px;
        letter-spacing: 0.03em;
        margin-left: 0.35rem;
    }
    .result-section-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #7a90b8;
        margin: 2.75rem 0 1.25rem 0;
    }
    .skill-list { margin: 0; padding: 0; list-style: none; }
    .skill-list li {
        font-size: 1.05rem;
        color: #c8d8ee;
        padding: 0.55rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .skill-list li::before {
        content: "";
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #ef4444;
        flex-shrink: 0;
    }
    .suggestion-row {
        display: flex;
        gap: 1.1rem;
        margin-bottom: 1.1rem;
        align-items: flex-start;
    }
    .suggestion-num {
        font-size: 0.85rem;
        font-weight: 700;
        color: #2563eb;
        min-width: 1.5rem;
        padding-top: 0.2rem;
        font-family: 'Inter', sans-serif !important;
    }
    .suggestion-text {
        font-size: 1.05rem;
        color: #c0d0e8;
        line-height: 1.7;
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Progress bar ── */
    div[data-testid="stProgressBar"] > div > div {
        border-radius: 99px;
    }
    div[data-testid="stProgressBar"] {
        background: #141a28 !important;
        border-radius: 99px;
    }

    /* ── Misc ── */
    .stAlert { border-radius: 8px; font-family: 'Inter', sans-serif !important; font-size: 1rem !important; }
    hr { border-color: #1a2236 !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div style="flex-shrink:0;">
        <svg width="52" height="52" viewBox="0 0 54 54" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="54" height="54" rx="13" fill="url(#hg)"/>
            <rect x="13" y="10" width="18" height="24" rx="2.5" fill="white" opacity="0.9"/>
            <path d="M27 10 L31 14 L27 14 Z" fill="#0a1a3e" opacity="0.3"/>
            <rect x="16" y="19" width="10" height="2" rx="1" fill="#2563eb"/>
            <rect x="16" y="23" width="13" height="2" rx="1" fill="#93c5fd" opacity="0.7"/>
            <rect x="16" y="27" width="8"  height="2" rx="1" fill="#93c5fd" opacity="0.45"/>
            <circle cx="34" cy="37" r="7.5" fill="#0c0e14" stroke="#2563eb" stroke-width="2.5"/>
            <circle cx="34" cy="37" r="3.5" fill="none" stroke="#60a5fa" stroke-width="2"/>
            <line x1="39.5" y1="42.5" x2="43" y2="46" stroke="#2563eb" stroke-width="3" stroke-linecap="round"/>
            <defs>
                <linearGradient id="hg" x1="0" y1="0" x2="54" y2="54" gradientUnits="userSpaceOnUse">
                    <stop offset="0%" stop-color="#0d2860"/>
                    <stop offset="100%" stop-color="#1d4ed8"/>
                </linearGradient>
            </defs>
        </svg>
    </div>
    <div>
        <h1>AI Job Screener</h1>
        <p class="app-tagline">Paste a job description, upload your resume, and get a match score with personalized tips to land the role.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Inputs ───────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.markdown('<p class="field-label">Job Description</p>', unsafe_allow_html=True)
    job_description = st.text_area(
        "Job Description",
        height=320,
        placeholder="Paste the job posting here...",
        label_visibility="collapsed",
    )

with col2:
    st.markdown('<p class="field-label">Resume</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")

resume = ""
if uploaded_file is not None:
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            resume += page.extract_text() or ""
    st.success("Resume uploaded successfully.")

st.markdown("<br>", unsafe_allow_html=True)
analyze_btn = st.button("Analyze Resume", type="primary", use_container_width=True)

# ── Analysis ─────────────────────────────────────────────────────────────────
if analyze_btn:
    if not job_description or not resume:
        st.warning("Please provide both a job description and your resume.")
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

        st.divider()

        # ── Score ─────────────────────────────────────────────────────────────
        score_match = re.search(r'\*\*Match Score:\*\*\s*(\d+)/100', result)
        score = int(score_match.group(1)) if score_match else None

        if score is not None:
            if score >= 70:
                color, badge_bg, badge_color, verdict = "#22c55e", "#0d2318", "#22c55e", "Strong Match"
            elif score >= 45:
                color, badge_bg, badge_color, verdict = "#f59e0b", "#231a07", "#f59e0b", "Moderate Match"
            else:
                color, badge_bg, badge_color, verdict = "#ef4444", "#230d0d", "#ef4444", "Needs Work"

            st.markdown(f"""
<div class="score-row">
    <span class="score-num" style="color:{color}">{score}</span>
    <span class="score-denom">/100</span>
    <span class="score-badge" style="background:{badge_bg};color:{badge_color}">{verdict}</span>
</div>
""", unsafe_allow_html=True)
            st.progress(score / 100)

        # ── Missing skills ────────────────────────────────────────────────────
        skills_match = re.search(
            r'\*\*Missing Skills/Qualifications:\*\*\s*((?:- .+\n?)+)', result
        )
        if skills_match:
            skills = [s.lstrip("- ").strip()
                      for s in skills_match.group(1).strip().splitlines() if s.strip()]
            items_html = "".join(f"<li>{s}</li>" for s in skills)
            st.markdown(f"""
<p class="result-section-title">Missing Skills &amp; Qualifications</p>
<ul class="skill-list">{items_html}</ul>
""", unsafe_allow_html=True)

        # ── Suggestions ───────────────────────────────────────────────────────
        suggestions_match = re.search(
            r'\*\*Suggestions to Improve Your Resume:\*\*\s*((?:- .+\n?)+)', result
        )
        if suggestions_match:
            suggestions = [s.lstrip("- ").strip()
                           for s in suggestions_match.group(1).strip().splitlines() if s.strip()]
            rows_html = "".join(
                f'<div class="suggestion-row">'
                f'<span class="suggestion-num">{i+1:02d}</span>'
                f'<span class="suggestion-text">{s}</span>'
                f'</div>'
                for i, s in enumerate(suggestions)
            )
            st.markdown(f"""
<p class="result-section-title">How to Improve Your Resume</p>
{rows_html}
""", unsafe_allow_html=True)

        # Fallback
        if score is None and not skills_match and not suggestions_match:
            st.markdown(result)
