# AI Job Application Screener

An AI-powered web app that analyzes how well your resume matches a job description. Paste in a job posting and your resume, and get back an instant match score, a list of missing skills, and specific suggestions to improve your application.

**Live Demo:** [https://jobscreener-ciosgbjjhtknewzejt9s38.streamlit.app/]

---

## Features

- **Match Score** — get a score from 0–100 showing how well your resume fits the role
- **Skill Gap Analysis** — identifies key qualifications from the job description missing from your resume
- **Actionable Suggestions** — specific recommendations to tailor your resume for the position
- **Instant Results** — powered by OpenAI GPT-4o for fast, accurate analysis

## How It Works

1. Paste a job description and your resume into the text boxes
2. Click **Analyze**
3. The app sends both to OpenAI's GPT-4o model with a prompt engineered to act as an expert hiring manager
4. The model returns a structured response with your match score, missing skills, and improvement suggestions
5. Results are rendered instantly in the UI
