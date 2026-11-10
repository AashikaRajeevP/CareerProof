import os
import uuid
from werkzeug.utils import secure_filename
import markdown
import bleach
import re
from flask import Flask,render_template,request,session
from resume_parser import extract_text_from_pdf,parse_resume
from ai_analyzer import analyze_job_match
from interview_generator import generate_interview_questions
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("SECRET_KEY is missing from .env")

UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union({
    "h1", "h2", "h3", "h4",
    "p", "hr", "ul", "ol", "li",
    "strong", "em", "code", "pre",
    "blockquote", "table", "thead",
    "tbody", "tr", "th", "td"
})

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "resume" not in request.files:
        return "No file uploaded."

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a PDF file."

    filename = secure_filename(file.filename)

    if not filename.lower().endswith(".pdf"):
        return "Only PDF files are allowed."

    unique_filename = f"{uuid.uuid4().hex}.pdf"

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_filename
    )

    try:
        file.save(file_path)

        # Your original functionality is preserved
        resume_text = extract_text_from_pdf(file_path)
        resume_data = parse_resume(resume_text)

        session["resume_data"] = resume_data

        return render_template(
            "results.html",
            resume=resume_data
        )

    except Exception as e:
        print("Resume upload error:", repr(e))
        return "Unable to process this PDF. Please try another file."

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@app.route("/analyze", methods=["POST"])
def analyze():

    job_description = request.form["job_description"]
    session["job_description"] = job_description

    resume_data = session.get("resume_data")

    if not resume_data:
        return "Please upload your resume first."

    ai_result = analyze_job_match(resume_data, job_description)

    ai_result = re.sub(r'\\([#*])', r'\1', ai_result)

    html_result = markdown.markdown(
        ai_result,
        extensions=["extra"]
    )

    safe_result = bleach.clean(
        html_result,
        tags=allowed_tags,
        strip=True
    )

    return render_template(
        "ai_results.html",
        ai_result=safe_result
    )


@app.route("/interview", methods=["POST"])
def interview():
    resume_data = session.get("resume_data")
    job_description = session.get("job_description")

    if not resume_data or not job_description:
        return "Please upload your resume and analyze a job description first."

    try:
        questions = generate_interview_questions(
            resume_data,
            job_description
        )

        if not questions or not questions.strip():
            raise ValueError("No questions were generated.")

        html_questions = markdown.markdown(
            questions,
            extensions=["extra"]
        )

        safe_questions = bleach.clean(
            html_questions,
            tags=allowed_tags,
            strip=True
        )

        return render_template(
            "interview_results.html",
            questions=safe_questions,
            error_message=None
        )

    except Exception as e:
        print("Interview generation error:", repr(e))

        return render_template(
            "interview_results.html",
            questions=None,
            error_message=(
                "We're having trouble generating your personalized "
                "interview questions right now. Please try again later. "
                "Your resume analysis is still available."
            )
        )


if __name__ == "__main__":
    app.run(debug=True)