from flask import Flask, request, jsonify
from pyresparser import ResumeParser

app = Flask(__name__)

@app.route('/', methods=['POST'])
def JDParser():
    req_json = request.json
    job_desc = req_json['desc']
    extracted_info = ResumeParser(job_desc, skills_file="custom_skills.csv").get_extracted_data()
    return jsonify({'Skills': extracted_info['skills']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)