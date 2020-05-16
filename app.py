from flask import Flask,render_template,request,jsonify
from functions import job_desc_extractor
from config import HOST,METHOD,PORT


app=Flask(__name__)



@app.route("/")
def before():
    return render_template("extract.html")

@app.route("/",methods=METHOD)
def after_extract():
    extracted_data=job_desc_extractor(request.form['desc'])

    return render_template("extract.html",
                           CompanyName=extracted_data['company'],
                           Title=extracted_data['title'],
                           Email=extracted_data['email'],
                           Urls=extracted_data['url'],
                           Salary=extracted_data['salary'],
                           Salary_min=extracted_data['salary_min'],
                           Salary_max=extracted_data['salary_max'],
                           Currency=extracted_data['currency'],
                           Vacancy=extracted_data['vacancy'],
                           Address=extracted_data['address'],
                           Skills=extracted_data['skills'],
                           Experience=extracted_data['experience'],
                           Deadline=extracted_data['deadline'],
                           Location=extracted_data['location'],
                           Qualification=extracted_data['qualification'],
                           JobNature=extracted_data['job_nature'])

@app.route('/api', methods= METHOD)
def api():
    extracted_info = job_desc_extractor(request.json['desc'])
    return jsonify({'extracted info': extracted_info})

if  (__name__)=="__main__":
    app.run(host=HOST, port=PORT)