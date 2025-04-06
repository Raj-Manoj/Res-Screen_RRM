
from flask import Flask, render_template, request
import os
from utils import jd_agent, resume_agent, email_agent

app = Flask(__name__, template_folder="../templates")
UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    jd_pdf = request.files.get('jd_pdf')
    resumes = request.files.getlist('resumes')

    jd_path = os.path.join(app.config['UPLOAD_FOLDER'], jd_pdf.filename)
    jd_pdf.save(jd_path)

    jd_text = jd_agent.extract_text_from_pdf(jd_path)
    jd_summary = jd_agent.summarize_jd(jd_text)

    candidates = []
    emails = []

    for resume in resumes:
        path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
        resume.save(path)
        parsed = resume_agent.parse_resume(path)
        if resume_agent.match_candidate(jd_text, parsed):
            candidates.append(parsed)
            emails.append(email_agent.generate_email(parsed['name'], jd_summary))

    return render_template('results.html', jd_summary=jd_summary, candidates=candidates, emails=emails)

def handler(environ, start_response):
    return app(environ, start_response)
