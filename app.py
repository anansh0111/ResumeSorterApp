from flask import Flask, render_template, request
import os
from matcher import match_resume_to_jd
from resume_parser import extract_text

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        jd_text = request.form['job_description']
        files = request.files.getlist('resumes')
        results = []

        for file in files:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            resume_text = extract_text(filepath)
            score = match_resume_to_jd(jd_text, resume_text)
            results.append({'name': file.filename, 'score': round(score * 100, 2)})

        results.sort(key=lambda x: x['score'], reverse=True)
        names = [r['name'] for r in results]
        scores = [r['score'] for r in results]

        return render_template('results.html', results=results, names=names, scores=scores)

    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
