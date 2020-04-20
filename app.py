from flask import Flask, request, jsonify, render_template
from pyresparser import ResumeParser
from config import METHOD, HOST, PORT
from skills import custom_skills

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods= METHOD)
def extract():
    extracted_skill = ResumeParser(request.form['desc'], skills_file=custom_skills).get_extracted_data()['skills']
    return render_template('index.html', skills = extracted_skill)

@app.route('/api', methods= METHOD)
def JDParser():
    extracted_info = ResumeParser(request.json['desc'], skills_file=custom_skills).get_extracted_data()
    return jsonify({'all': extracted_info})

@app.route('/data-generator')
def data_generator():
    return app.send_static_file('data-generator.html')

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)