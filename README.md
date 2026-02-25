# AI Job Application Screener

An AI-powered web app that analyzes how well your resume matches a job description. Paste in a job posting and your resume, and get back an instant match score, a list of missing skills, and specific suggestions to improve your application.

**Live Demo:** [your-app.streamlit.app](https://your-app.streamlit.app) ← replace with your actual URL

---

## Features

- **Match Score** — get a score from 0–100 showing how well your resume fits the role
- **Skill Gap Analysis** — identifies key qualifications from the job description missing from your resume
- **Actionable Suggestions** — specific recommendations to tailor your resume for the position
- **Instant Results** — powered by OpenAI GPT-4o for fast, accurate analysis

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web UI framework |
| OpenAI API (GPT-4o) | AI analysis engine |
| python-dotenv | Secure API key management |

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/MarkGad23/job_screener.git
cd job_screener
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your OpenAI API key
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_api_key_here
```
Get your API key at [platform.openai.com](https://platform.openai.com)

### 4. Run the app
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## How It Works

1. Paste a job description and your resume into the text boxes
2. Click **Analyze**
3. The app sends both to OpenAI's GPT-4o model with a prompt engineered to act as an expert hiring manager
4. The model returns a structured response with your match score, missing skills, and improvement suggestions
5. Results are rendered instantly in the UI

---

## Project Structure

```
job_screener/
├── app.py              # Main application
├── requirements.txt    # Dependencies
├── .env                # API key (not committed)
└── .gitignore
```

---

## Security

API keys are managed via environment variables and never committed to version control. On Streamlit Cloud, secrets are stored securely in the app settings.
