
import os
from flask import Flask, render_template, request
from utils import jd_agent, resume_agent, email_agent, db_handler

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    jd_file = request.files['jd_file']
    resume_files = request.files.getlist('resumes')
    jd_path = os.path.join(UPLOAD_FOLDER, jd_file.filename)
    jd_file.save(jd_path)

    jd_text = jd_agent.extract_text(jd_path)
    jd_summary = jd_agent.summarize_jd(jd_text)

    shortlisted = []
    for resume in resume_files:
        path = os.path.join(UPLOAD_FOLDER, resume.filename)
        resume.save(path)
        parsed = resume_agent.parse_resume(path)
        if resume_agent.match_candidate(parsed, jd_summary):
            shortlisted.append(parsed)

    emails = [email_agent.generate_email(c) for c in shortlisted]
    db_handler.save_candidates(shortlisted)

    return render_template('results.html', jd_summary=jd_summary, candidates=shortlisted, emails=emails)

if __name__ == '__main__':
    app.run(debug=True)
