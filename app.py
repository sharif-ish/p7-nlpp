from flask import Flask, request, jsonify, render_template
from pyresparser import ResumeParser
from config import METHOD, HOST, PORT
from skills import custom_skills

app = Flask(__name__)

def parser(get_data):
    extracted_info = ResumeParser(get_data['desc'], skills_file=custom_skills).get_extracted_data()
    return extracted_info

@app.route('/', methods= METHOD)
def JDParser():
    extracted_info = parser(request.json)
    return jsonify({'all': extracted_info})

@app.route('/skills')
def home():
    return render_template('index.html')

@app.route('/skills', methods= METHOD)
def extract():
    extracted_skill = parser(request.form)['skills']
    return render_template('index.html', skills = extracted_skill)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)