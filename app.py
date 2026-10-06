from flask import Flask,render_template,request
from resume_parser import extract_text_from_pdf,parse_resume

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")
@app.route("/upload",methods=["POST"])
def upload():
    file=request.files["resume"]
    file_path="uploads/"+file.filename
    file.save(file_path)
    resume_text=extract_text_from_pdf(file_path)
    resume_data = parse_resume(resume_text)
 #  return ("Resume uploaded successfully")
    return str(resume_data)


if __name__ == "__main__":
    app.run(debug=True)