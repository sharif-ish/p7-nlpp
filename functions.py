import re
import datefinder
import nltk
from from_external_api import custom_skills
from urlextract import URLExtract
from difflib import SequenceMatcher
from config import matching_ratio

# Returns a list, containing longest matched substrings
def longest_matched_substring(text, entity_list):
    substrings = []
    for entity in entity_list:
        entity = entity.lower()
        match = SequenceMatcher(None, text, entity).find_longest_match(0, len(text), 0, len(entity))
        matched_substring = text[match.a: match.a + match.size]
        ratio = SequenceMatcher(None, matched_substring, entity).ratio()
        if ratio >= matching_ratio:
            substrings.append(matched_substring)
    return substrings

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
    company_file = open("company_name.txt", encoding="utf-8").read()
    company_list = eval(company_file)
    company_list = [i.lower() for i in company_list]
    text=text.replace('\n'," ").replace('.','').lower()

    complst=[]
    for company in company_list:
        if ' ' + remove_extra_word(company.replace('.', '')) in ' '+text+ ' ':
            complst.append(company.title())
    return complst


def extract_title(text):
    title_file = open("title.txt")  # Title file
    title_list = [line.strip('\n') for line in title_file.readlines()]
    job_titles = []
    for title in title_list:
        if title.lower() in text.lower():
            job_titles.append(title)
    return job_titles

#Function to extract Salary
def extract_salary(text):
    pattern = re.compile(r'\b(?:Salary|Compensation|Allowance).*\n?.*',flags=re.I)
    match = re.findall(pattern, text)
    print(match)
    match = re.sub(r"([,\\nr])", "", str(match))
    salary_pattern = re.compile(r'\d+\w?')
    salary = re.findall(salary_pattern, match)

    currency_file = open("currency.txt", encoding="utf-8").read()
    currency_list = eval(currency_file)

    for cur in currency_list:
        if ' '+cur.lower()+' ' in match.lower():
            currency = cur
        else:
            currency = None

    if len(salary) > 1:
        salary = {'minimum' : salary[0], 'maximum' : salary[1]}
    else:
        salary =  salary
    return {'salary': salary, 'currency' : currency}


#Function to extract Email
def extract_email(text):
    pattern = re.compile(r"[A-Za-z0-9\.\-+_]+@[A-Za-z0-9\.\-+_]+\.[A-Za-z]+")
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
        if skill.lower() in text.lower():
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
         "salary":extract_salary(text)['salary'],
          "currency":extract_salary(text)['currency'],
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