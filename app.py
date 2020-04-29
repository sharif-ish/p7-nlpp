from flask import Flask, request, jsonify, render_template
from config import METHOD, HOST, PORT
from functions import job_desc_extractor
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api', methods= METHOD)
def JDParser():
    extracted_info = job_desc_extractor(request.form['desc'])
    return jsonify({'all': extracted_info})

@app.route('/extract')
def before_extract():
    return render_template('extract.html')

@app.route('/extract', methods= METHOD)
def after_extract():
    extracted_info = job_desc_extractor(request.form['desc'])
    return render_template('extract.html',
                           title =extracted_info['Title'],
                           salary=extracted_info['Salary'],
                           email=extracted_info['Email'],
                           location=extracted_info['Location'],
                           skills=extracted_info['Skills'],
                           company_names=extracted_info['Company Name'],
                           qualification=extracted_info['Qualification'],
                           experience=extracted_info['Experience']
                           )

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)