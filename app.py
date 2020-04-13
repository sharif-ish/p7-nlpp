from flask import Flask, request, jsonify, render_template
from pyresparser import ResumeParser
from config import METHOD, HOST, PORT
from skills import custom_skills

app = Flask(__name__)

@app.route('/', methods= METHOD)
def JDParser():
    req_json = request.json
    job_desc = req_json['desc']
    extracted_info = ResumeParser(job_desc, skills_file=custom_skills).get_extracted_data()
    return jsonify({'all': extracted_info})

@app.route('/ui')
def home():
    return render_template('index.html')

@app.route('/ui', methods= METHOD)
def extract():
    job_desc = request.form['desc']
    extracted_info = ResumeParser(job_desc, skills_file=custom_skills).get_extracted_data()
    extracted_skill = extracted_info['skills']
    return render_template('index.html', skills = extracted_skill)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)