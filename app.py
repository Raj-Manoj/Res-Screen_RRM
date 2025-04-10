import os
from flask import Flask, request, render_template
from utils import jd_agent, resume_agent, email_agent

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    jd_file = request.files['jd_file']
    resumes = request.files.getlist('resumes')

    jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_file.filename)
    jd_file.save(jd_path)
    jd_text = jd_agent.extract_text_from_pdf(jd_path)
    jd_summary = jd_agent.summarize_jd(jd_text)

    parsed_resumes = []
    for resume in resumes:
        path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
        resume.save(path)
        parsed = resume_agent.parse_resume(path)
        parsed_resumes.append(parsed)

    shortlisted = resume_agent.match_candidate(jd_summary, parsed_resumes)
    emails = [email_agent.generate_email(candidate) for candidate in shortlisted]

    return render_template('results.html', candidates=shortlisted, emails=emails)

if __name__ == '__main__':
    app.run(debug=True)
