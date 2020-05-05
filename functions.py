import re
import datefinder
import nltk
from from_external_api import custom_skills
from urlextract import URLExtract

#Function to remove extra words
def remove_extra_word(text):
    if len(text.split())<3:
        return text
    else:
        rmlst=['ltd','limited','inc','pvt']
        for r in rmlst:
            if ' '+r in text:
                text=text.replace(' '+r,'')
        return text


#Function to extract Company Name
def extract_company(text):
    company_file=open('company_name.txt').readlines()
    company_list=[comp.split(',') for comp in company_file]
    company_list=[comp.strip() for company in company_list for comp in company]
    text=text.replace('\n'," ").replace('.','').lower()

    complst=[]
    for company in company_list:
        if ' ' + remove_extra_word(company.replace('.', '')) in ' '+text+ ' ':
            complst.append(company.title())
    return complst


def extract_title(text):
    title_file = open("title.txt")  # Title file
    title_list = [line.strip('\n').lower() for line in title_file.readlines()]

    for title in title_list:
        if title in text.lower():
            return title.title()
            break

#Function to extract Salary
def extract_salary(text):
    pattern = re.compile(r'\b(?:Salary|Compensation|Allowance).*\n?.*',flags=re.I)
    match = re.findall(pattern, text)
    sub_newline = re.sub(r'\\n', ' ', str(match))
    sub_newline = re.sub(r',', '', sub_newline)
    new_pattern = re.compile(r'\d+\w?')
    salary = re.findall(new_pattern, sub_newline)

    if len(salary) > 1:
        if len(re.sub('\d', '', salary[0])) == 0:
            unit = re.sub('\d', '', salary[1])
        else:
            unit = ''
        return ("Minimum Salary:", salary[0] + unit, "Maximum Salary:", salary[1])
    elif len(salary) == 1:
        return ("Salary:", salary[0])
    else:
        return ("Negotiable")

#Function to extract Currency
def extract_currency(text):
    pattern = re.compile(r'\b(?:Salary|Compensation|Allowance).*\n?.*',flags=re.I)
    match = re.findall(pattern, text)
    sub_newline = re.sub(r'\\n', ' ', str(match))
    sub_newline = re.sub(r',', '', sub_newline)

    currency = set()
    currency_file = open("currency.txt").readlines()
    currency_list = [line.split(',') for line in currency_file]
    currency_list = [cur for currency in currency_list for cur in currency]

    for cur in currency_list:
        if cur in sub_newline:
            currency.add(cur)
    if len(currency) > 0:
        return currency
    else:
        return "BDT"

#Function to extract Email
def extract_email(text):
    pattern=re.compile(r'\S+@\S+')
    match=re.findall(pattern,text)
    return match
#Function to extract Urls
def extract_url(text):
    return URLExtract().find_urls(text)

#Function to extract the vacancy
def extract_vacancy(text):
    pattern=re.compile(r'.*vacancy.*\n?.*',flags=re.I)
    match=re.findall(pattern,text)
    sub_newline=re.sub(r'\\n',' ',str(match))
    vacancy=re.findall(r'\d+',str(sub_newline))
    return vacancy

#Function for extracting skills
def extract_skill(text):
    skill_list=[]
    for skill in custom_skills:
        if skill in text.lower():
            skill_list.append(skill.title())
    return skill_list

#Function for extracting experience
def extract_experience(text):
    pattern=re.compile(r'.*Experience.*\n?.*',flags=re.I)
    match=re.findall(pattern,text)
    sub_newline=re.sub(r'\\n',' ',str(match))
    experience=re.findall(r'\d ?-?t?o?\+? ?\d? ?\S+',str(sub_newline))
    if len(experience)>0:
        return experience[0]
    else:
        return experience


# Function for extracting deadline
def extract_deadline(text):
    deadline=[]
    pattern=re.compile(r'.*(?:january|february|march|april|may|june|july|august|septrmber|november|december).*|(?:\d+[\./]\d+[\./]\d+)',flags=re.I)
    match=re.findall(pattern,text)#returns a list
    text=' '.join([str(m) for m in match])#concerting to string
    matches = datefinder.find_dates(text.replace(':',''))#converting the":" punctuation
    for mat in matches:
        deadline.append(mat)
    if len(deadline)==0:
        return deadline
    else:
        return deadline[0].strftime("%x")
    return deadline

#Function to extract location
def extract_location(text):
    location = set()

    location_file = open("location.txt").readlines()
    location_list = [line.split(',') for line in location_file]
    location_list=[l for loc in location_list for l in loc]

    for l in location_list:
        if l in text.lower():
            location.add(l.title())

    return list(location)

# Function to extract the qualification
def extract_qualification(text):
    pattern = re.compile(r'Education\w+ ?\w+.*\n?\S.*',flags=re.I)
    match = re.findall(pattern, text)
    sub_newline = re.sub(r'\\n', ' ', str(match))
    sub_non_alphabet = re.sub('[^A-Za-z ]', "", str(sub_newline))
    qulification_list = ['bsc', 'msc', 'masters', 'diploma', 'Polytechnic']
    dept_name = ['cse', 'cis', 'csse', 'eee', 'computer application', 'computer', 'computer science']
    word = nltk.word_tokenize(sub_non_alphabet)
    qulification = []
    dept = []
    for w in word:
        if w.lower() in qulification_list:
            qulification.append(w)
    for w in word:
        if w.lower() in dept_name:
            dept.append(w)
    qulification = '/'.join(qulification)
    dept = ' '.join(dept)
    if len(qulification) == 0 and len(dept) == 0:
        return "Not applicable"
    elif len(qulification) == 0 and len(dept) > 0:
        qulification = "BSC"
        return qulification + " in " + dept
    else:
        return qulification + " in " + dept

#Function to extract the job nature
def extract_job_nature(text):
    job_type=['internship','contractual','full-time', 'permanent']
    job_nature=[]
    for job in job_type:
        if job in text.lower():
            job_nature.append(job.title())
    if len(job_nature)>0:
        return job_nature
    else:
        return "Full time"


def job_desc_extractor(text):
    data={"company":extract_company(text),
        "title":extract_title(text),
         "salary":extract_salary(text),
          "currency":extract_currency(text),
          "email":extract_email(text),
          "url":extract_url(text),
          "vacancy":extract_vacancy(text),
          "skills":extract_skill(text),
          "experience":extract_experience(text),
          "deadline":extract_deadline(text),
          "location":extract_location(text),
          "qualification":extract_qualification(text),
          "job_nature":extract_job_nature(text)
          }
    return data