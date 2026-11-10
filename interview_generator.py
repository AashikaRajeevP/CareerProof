import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=45000)
)


def generate_interview_questions(resume_data, job_description):

    prompt = f"""
    You are CareerProof, an AI interview preparation assistant.

    Generate personalised interview questions using the candidate's
    resume and the job description.

    RESUME:
    {resume_data}

    JOB DESCRIPTION:
    {job_description}

    Generate exactly 13 questions in these categories:

    1. RESUME-BASED QUESTIONS (3)
    Ask about skills, education and experience mentioned in the resume.

    2. TECHNICAL QUESTIONS (4)
    Ask technical questions based on the job requirements and the
    candidate's listed skills.

    3. PROJECT DEEP-DIVE QUESTIONS (3)
    Ask about actual projects, technologies, implementation,
    challenges and design decisions.

    4. HR AND BEHAVIORAL QUESTIONS (3)
    Ask about teamwork, problem-solving, motivation and career goals.

    RULES:
    - Personalise questions using the actual resume and job description.
    - Never invent projects, skills or experience.
    - Avoid generic questions when specific resume details are available.
    - Questions should be suitable for a fresher attending placements.
    - Do not provide answers.
    - Number questions within each category.
    - Keep questions clear and concise.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=2000
        )
    )

    return response.text
