import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError
from google.genai import types


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(timeout=45000)
)

import re

def basic_resume_analysis(resume_data, job_description):

    known_skills = [
        "Python", "Java", "C", "C++", "Flask", "Django",
        "HTML", "CSS", "JavaScript", "React", "Node.js",
        "SQL", "MySQL", "PostgreSQL", "MongoDB",
        "REST APIs", "Git", "GitHub", "Docker",
        "Machine Learning", "Data Structures"
    ]

    skills = resume_data.get("skills", [])
    projects = resume_data.get("projects", [])
    experience = resume_data.get("experience", [])

    def contains_keyword(text, keyword):
        pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"
        return bool(re.search(pattern, str(text), re.IGNORECASE))

    required_skills = []

    for skill in known_skills:
        if contains_keyword(job_description, skill):
            required_skills.append(skill)

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        if any(contains_keyword(s, skill) for s in skills):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    project_evidence = []

    for project in projects:
        description = project.get("description", "")
        name = project.get("name", "Unnamed project")

        project_evidence.append({
            "name": name,
            "description": description
        })

    experience_text = " ".join(str(item) for item in experience)

    # SECTION 1: Matching skills
    result = """

> **Basic Analysis Mode:** Gemini AI is unavailable.
> This report uses rule-based keyword matching.

## 1. Matching Skills
"""

    if matched_skills:
        for skill in matched_skills:
            result += f"\n- **{skill}**"
    else:
        result += "\nNo matching skills found."

    # SECTION 2: Missing skills
    result += "\n\n## 2. Skills Not Mentioned\n"

    if missing_skills:
        for skill in missing_skills:
            result += f"\n- **{skill}**"
    else:
        result += "\nNo missing skills found."

    # SECTION 3: Skill evidence
    result += "\n\n## 3. Skill Evidence\n"

    for skill in required_skills:

        evidence = []

        if any(contains_keyword(s, skill) for s in skills):
            evidence.append("Listed in technical skills")

        for project in project_evidence:
            if contains_keyword(project["description"], skill):
                evidence.append(
                    f"Found in project: {project['name']}"
                )

        if contains_keyword(experience_text, skill):
            evidence.append("Found in experience")

        if any("Found in project" in item or item == "Found in experience"
               for item in evidence):
            classification = "Demonstrated in resume content"
        elif evidence:
            classification = "Claimed - listed in skills only"
        else:
            classification = "Not mentioned"

        result += f"\n- **{skill}: {classification}**"

        if evidence:
            result += "\n  - " + "; ".join(evidence)

    # SECTION 4: Project relevance
    result += "\n\n## 4. Project Relevance\n"

    if not project_evidence:
        result += "\nNo project information was found in the resume."

    else:
        for project in project_evidence:

            description = project["description"]
            relevant_skills = [
                skill for skill in required_skills
                if contains_keyword(description, skill)
            ]

            result += f"\n### {project['name']}\n"

            if not description.strip():
                result += (
                    "\nThe project has no description in the resume. "
                    "Its technical relevance cannot be assessed."
                )

            elif relevant_skills:
                result += (
                    "\nJob-related technologies mentioned: "
                    + ", ".join(relevant_skills)
                )
                result += (
                    "\nThis project contains textual evidence "
                    "related to the job requirements."
                )

            else:
                result += (
                    "\nNo direct keyword overlap with the identified "
                    "job skills was found in the project description."
                )

    # SECTION 5: Specific improvement suggestions
    result += "\n\n## 5. Improvement Suggestions\n"

    suggestions = {
        "Python": "Describe the Python features or logic you implemented in your projects.",
        "Flask": "Mention Flask routes, request handling, backend features or template rendering you implemented.",
        "Django": "If you have used Django, include a project or practical example demonstrating it.",
        "SQL": "Name the database you used and describe the queries or database operations you performed.",
        "MySQL": "Mention how you designed tables, queried data or connected MySQL to an application.",
        "PostgreSQL": "Describe any PostgreSQL database design or integration experience you have.",
        "REST APIs": "If you developed or integrated APIs, explain the endpoints, requests and responses you handled.",
        "JavaScript": "Describe interactive features or frontend functionality you implemented using JavaScript.",
        "HTML": "Mention the pages, forms or layouts you created using HTML.",
        "CSS": "Describe the styling, layouts or responsive design you implemented using CSS.",
        "Git": "Mention how you used Git for commits, branching and version control.",
        "GitHub": "Include relevant GitHub repositories and explain your contributions.",
        "MongoDB": "Describe the collections, queries or database operations you implemented.",
        "React": "Mention the components and frontend functionality you built using React.",
        "Node.js": "Describe the backend functionality or APIs you implemented using Node.js.",
        "Docker": "If applicable, explain how you containerized or ran your application using Docker.",
        "Machine Learning": "Mention the model, dataset and task involved in your machine learning work.",
        "Data Structures": "Include examples of how you applied data structures to solve programming problems.",
        "Java": "Describe a project or programming task where you applied Java.",
        "C": "Include examples of C programs or systems concepts you implemented.",
        "C++": "Describe the C++ programs or object-oriented concepts you have applied."
    }

    if missing_skills:
        result += "\n**Requirements not mentioned in your resume:**\n"

        for skill in missing_skills:
            suggestion = suggestions.get(
                skill,
                "If you have this skill, add a practical example demonstrating its use."
            )

            result += f"\n- **{skill}:** {suggestion}"

    if matched_skills:
        result += "\n\n**Improve evidence for matching skills:**\n"

        for skill in matched_skills:
            if not any(
                contains_keyword(project["description"], skill)
                for project in project_evidence
            ) and not contains_keyword(experience_text, skill):

                result += (
                    f"\n- **{skill}:** This skill is listed, "
                    "but no supporting project or experience description "
                    "was found. Add a genuine example of how you used it."
                )

    if not missing_skills and not matched_skills:
        result += "\nAdd relevant technical skills and supporting project evidence to your resume."

    result += """

> **Note:** This analysis uses keyword matching. A skill mentioned
> in a project or experience description is treated as textual evidence,
> not proof of proficiency. Project relevance is based on keyword overlap,
> not a full understanding of the project.
"""

    return result


def analyze_job_match(resume_data, job_description):

    prompt = f"""
    You are CareerProof, a technical career analyst.

    Compare the candidate's resume with the job description.

    RESUME:
    {resume_data}

    JOB DESCRIPTION:
    {job_description}

    Provide these five sections:

    1. MATCHING SKILLS
    List skills found in both.

    2. MISSING SKILLS
    List job requirements not mentioned in the resume.
    Do not assume the candidate lacks these skills.

    3. SKILL EVIDENCE
    Classify important skills as:
    - Demonstrated: Supported by projects or experience.
    - Claimed: Listed but not supported by evidence.
    - Not Mentioned: No evidence found.

    4. PROJECT RELEVANCE
    Evaluate how relevant the candidate's projects are to the job.

    5. IMPROVEMENT SUGGESTIONS
    Give practical, specific resume improvement suggestions.

    Rules:
    - Never invent skills or experience.
    - Base conclusions only on the supplied resume.
    - Use concise bullet points.
    - Avoid repeating information.
    - Keep the complete analysis under 700 words.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=2000
            )
        )

        print("FINISH REASON:", response.candidates[0].finish_reason)
        print("USAGE:", response.usage_metadata)
        print("FULL GEMINI RESPONSE:", repr(response.text))

        return response.text

    except Exception as e:
        print("Gemini unavailable:", repr(e))
        return basic_resume_analysis(resume_data, job_description)
            