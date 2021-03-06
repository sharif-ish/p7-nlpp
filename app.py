from flask import Flask,render_template,request
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
                           Currency=extracted_data['currency'],
                           Vacancy=extracted_data['vacancy'],
                           Skills=extracted_data['skills'],
                           Experience=extracted_data['experience'],
                           Deadline=extracted_data['deadline'],
                           Location=extracted_data['location'],
                           Qualification=extracted_data['qualification'],
                           JobNature=extracted_data['job_nature'])


if  (__name__)=="__main__":
    app.run(host=HOST, port=PORT)