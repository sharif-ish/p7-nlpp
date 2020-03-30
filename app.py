from flask import Flask, request, jsonify
from pyresparser import ResumeParser
from config import METHOD, HOST, PORT
from skills import custom_skills

app = Flask(__name__)

@app.route('/', methods= METHOD)
def JDParser():
    req_json = request.json
    job_desc = req_json['desc']
    extracted_info = ResumeParser(job_desc, skills_file=custom_skills).get_extracted_data()
    return jsonify({'Skills': extracted_info['skills']})

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)