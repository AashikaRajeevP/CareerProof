# CareerProof – AI-Powered Resume Analyzer & Interview Preparation

**Don't just claim it. Prove it.**

CareerProof is an AI-powered platform that helps users analyze their resumes against job descriptions and prepare for interviews.

It identifies matching and missing skills, provides resume improvement suggestions, and generates personalized interview questions based on the user's resume and target job description.

## Features

- **Resume Parsing:** Upload a PDF resume and extract skills, education, projects, and experience.
- **AI-Powered Job Matching:** Analyze resumes against job descriptions using Google Gemini.
- **Skill Gap Analysis:** Identify matching and missing skills.
- **Improvement Suggestions:** Get recommendations to improve resume alignment with job requirements.
- **Interview Preparation:** Generate personalized interview questions.
- **Rule-Based Fallback:** Provides basic resume analysis when Gemini is unavailable.
- **Secure File Handling:** Validate PDF uploads and remove temporary files.

## Tech Stack

| Component | Technologies |
|---|---|
| Backend | Python, Flask |
| AI Integration | Google Gemini API |
| Frontend | HTML, CSS |
| PDF Processing | PyMuPDF |
| Other Libraries | Markdown, Bleach, python-dotenv |

## Project Structure

```text
ResumeProof/
│
├── app.py
├── resume_parser.py
├── ai_analyzer.py
├── interview_generator.py
├── requirements.txt
│
├── templates/
│   ├── index.html
│   ├── results.html
│   ├── ai_results.html
│   └── interview_results.html
│
├── test_ai_analyzer.py
├── test_gemini.py
└── test_interview_generator.py
```

## Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/AashikaRajeevP/CareerProof
```

**2. Navigate to the project folder**

```bash
cd ResumeProof
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_secret_key
```

**5. Run the application**

```bash
python app.py
```

Open your browser and visit `http://127.0.0.1:5000/`.

## Application Workflow

1. Upload a PDF resume.
2. Extract and organize resume information.
3. Enter a target job description.
4. Analyze matching skills and identify skill gaps.
5. Review improvement suggestions.
6. Generate personalized interview questions.

## Author

Developed as a Computer Science and Engineering project.

---

**CareerProof – Don't just claim it. Prove it.**