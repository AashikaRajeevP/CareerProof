from interview_generator import generate_interview_questions

# Sample resume data
resume_data = {
    "skills": ["Python", "Java", "Flask", "HTML", "CSS", "JavaScript", "MongoDB"],
    "projects": [
        {
            "name": "Pause-Scroll",
            "description": "An Android digital wellbeing application using Kotlin, Jetpack Compose and Accessibility Service to detect excessive scrolling."
        },
        {
            "name": "MediBot",
            "description": "A medical chatbot using Node.js, Express and Gemini API."
        },
        {
            "name": "CareerProof",
            "description": "A Flask application that analyses resumes against job descriptions using Gemini AI."
        }
    ],
    "experience": [],
    "education": ["B.Tech Computer Science and Engineering"]
}

job_description = """
Python Backend Developer

Requirements:
- Python programming
- Flask or Django
- SQL and database management
- REST API development
- HTML, CSS and JavaScript
- Git and GitHub
- Object-oriented programming
"""

try:
    questions = generate_interview_questions(
        resume_data,
        job_description
    )

    print("\n===== PERSONALISED INTERVIEW QUESTIONS =====\n")
    print(questions)

except Exception as e:
    print("Interview question generation failed:", repr(e))
