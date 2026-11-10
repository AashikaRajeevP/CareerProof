from ai_analyzer import analyze_job_match

resume_data = {
    "skills": ["Python", "Flask", "HTML", "CSS"],
    "projects": [
        {
            "name": "MediBot",
            "description": "Built a medical chatbot using Python and AI."
        }
    ],
    "education": ["B.Tech Computer Science"],
    "experience": []
}

job_description = """
We are looking for a Python developer with experience
in Flask, Django, SQL, REST APIs and JavaScript.
"""

result = analyze_job_match(resume_data, job_description)

print("\nCAREERPROOF AI ANALYSIS\n")
print(result)