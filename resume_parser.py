
import pymupdf
import re


def extract_text_from_pdf(pdf_path):
    document = pymupdf.open(pdf_path)

    blocks = []

    for page in document:
        page_blocks = page.get_text("blocks")

        for block in page_blocks:
            block_text = block[4].strip()

            if block_text:
                blocks.append(block_text)

    document.close()

    return "\n\n".join(blocks)


def parse_resume(text):
    resume_data = {
        "skills": [],
        "projects": [],
        "education": [],
        "experience": []
    }

    current_section = None
    current_project = None

    sections = [
        "SKILLS", "TECHNICAL SKILLS",
        "PROJECTS", "PROJECT EXPERIENCE",
        "EDUCATION", "ACADEMIC BACKGROUND",
        "EXPERIENCE", "WORK EXPERIENCE",
        "PROFESSIONAL EXPERIENCE",
        "INTERNSHIP / EXPERIENCE",
        "INTERNSHIP", "INTERNSHIPS",
        "CERTIFICATIONS & ACTIVITIES",
        "ADDITIONAL INFORMATION",
        "ADDITIONAL DETAILS",
        "ACHIEVEMENTS", "LANGUAGES", "INTERESTS"
    ]

    blocks = [
        block.strip()
        for block in text.split("\n\n")
        if block.strip()
    ]

    continuation_words = (
        "developed", "built", "created", "designed",
        "implemented", "worked", "collaborated",
        "responsible", "used", "practised",
        "managed", "assisted", "participated",
        "expected graduation", "graduation",
        "cgpa", "gpa", "currently pursuing"
    )

    for block in blocks:
        lines = [
            line.strip()
            for line in block.splitlines()
            if line.strip()
        ]

        if not lines:
            continue

        heading = lines[0].upper()

        # Detect section headings
        if len(lines) == 1 and heading in sections:

            if heading in ["SKILLS", "TECHNICAL SKILLS"]:
                current_section = "skills"

            elif heading in ["PROJECTS", "PROJECT EXPERIENCE"]:
                current_section = "projects"

            elif heading in ["EDUCATION", "ACADEMIC BACKGROUND"]:
                current_section = "education"

            elif heading in [
                "EXPERIENCE", "WORK EXPERIENCE",
                "PROFESSIONAL EXPERIENCE",
                "INTERNSHIP / EXPERIENCE",
                "INTERNSHIP", "INTERNSHIPS"
            ]:
                current_section = "experience"

            else:
                current_section = None

            current_project = None
            continue

        # Skills
        if current_section == "skills":
        # Join words split by PDF line wrapping
            skill_text = re.sub(
                r"(?<=\w)-\s*\n\s*(?=\w)",
                "",
                block
            )

            resume_data["skills"].append(
                " ".join(skill_text.split())
            )

        # Projects
        elif current_section == "projects":

            first_line = lines[0]

            numbered = re.match(r"^\d+[\.\)]\s+", first_line)

            if numbered:
                project_name = re.sub(
                    r"^\d+[\.\)]\s+", "", first_line
                )

                current_project = {
                    "name": project_name,
                    "description": " ".join(lines[1:])
                }

                resume_data["projects"].append(current_project)

            elif first_line.lower().startswith(continuation_words):
                if current_project:
                    current_project["description"] += " " + " ".join(lines)

            else:
                current_project = {
                    "name": first_line,
                    "description": " ".join(lines[1:])
                }

                resume_data["projects"].append(current_project)

        # Education
        elif current_section == "education":

            entry = " ".join(lines)

            if (
                resume_data["education"]
                and lines[0].lower().startswith(
                    ("expected graduation", "graduation", "cgpa", "gpa")
                )
            ):
                resume_data["education"][-1] += " " + entry

            else:
                resume_data["education"].append(entry)

        # Experience
        elif current_section == "experience":

            entry = " ".join(lines)

            if (
                resume_data["experience"]
                and lines[0].lower().startswith(continuation_words)
            ):
                resume_data["experience"][-1] += " " + entry

            else:
                resume_data["experience"].append(entry)

    return resume_data
