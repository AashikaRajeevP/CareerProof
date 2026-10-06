import fitz


def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()
    return text

def parse_resume(text):
    resume_data = {
        "skills": [],
        "projects": [],
        "education": [],
        "experience": []
    }

    current_section = None

    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.upper() in ["SKILLS", "TECHNICAL SKILLS"]:
            current_section = "skills"

        elif line.upper() in ["PROJECTS", "PROJECT EXPERIENCE"]:
            current_section = "projects"

        elif line.upper() in ["EDUCATION", "ACADEMIC BACKGROUND"]:
            current_section = "education"

        elif line.upper() in ["EXPERIENCE", "WORK EXPERIENCE", "PROFESSIONAL EXPERIENCE"]:
            current_section = "experience"

        else:
            if current_section:
                resume_data[current_section].append(line)

    return resume_data