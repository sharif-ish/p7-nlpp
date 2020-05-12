import re
import datefinder
from from_external_api import custom_skills
from urlextract import URLExtract
from difflib import SequenceMatcher
from config import matching_ratio

# Function to remove punctuation and convert to lower case
def text_cleaner(text):
    cleaned = re.sub('[-)(#$%*~:,?_+=@.]',' ',text)
    cleaned = cleaned.lower()
    return cleaned

# Function to remove punctuation and convert to lower case
def entity_matcher(text, entity_list, pattern):
    text = re.sub('[\n\r]',' ', str(text))
    matched_entities = []
    print(text)

    for entity in entity_list:
        if ' '+entity.lower()+' ' in ' '+text+' ':
            matched_entities.append(entity)

    if len(matched_entities) == 1:
        matched_entity = matched_entities[0]
    elif len(matched_entities) == 0:
        matched_entity = "Not Found"
    else :
        text = pattern_matcher(text, pattern)
        text = " ".join(text)
        ent = company_name_matcher(text, entity_list)
        matched_entity = str(ent)
    return matched_entity

# Function to match pattern
def pattern_matcher(text, pattern):
    compiled_pattern = re.compile(pattern, flags=re.I)
    match = re.findall(compiled_pattern, text)
    return match

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

#Function to remove extra words in company name
def extra_word_remover(company):
    text_without_word = re.sub('[.]','',company).lower()
    if len(text_without_word.split())<3:
        return company
    else:
        rmlst=['ltd','limited','inc','pvt']
        for r in rmlst:
            if ' '+r+' ' in ' '+text_without_word+' ':
                text_without_word = text_without_word.replace(' '+r,'')
        return text_without_word

# Function to match company name
def company_name_matcher(text, company_list):
    text = re.sub('[\n\r]',' ', str(text))
    complst = []

    for c in company_list:
        if ' '+c.lower()+' ' in ' '+text+' ':
            complst.append(c)
    return complst

#Function to extract Company Name
def extract_company(text):
    company_file = open("company_name.txt", encoding="utf-8").read()
    company_list =eval(company_file)
    complst = company_name_matcher(text, company_list)
    if len(complst) == 1:
        company_name = complst[0]
    elif len(complst) == 0:
        company_name = "Not Found"
    else :
        text = pattern_matcher(text, r'.*\b(?:company|looking for|is an|is a|is hiring).*\n?.*')
        text = " ".join(text)
        company = company_name_matcher(text, company_list)
        company_name = str(company)
    return company_name

#Function to extract title
def extract_title(text):
    title_file = open("title.txt")  # Title file
    title_list = [line.strip('\n') for line in title_file.readlines()]
    title_pattern = r'.*\b(?:looking for|searching for|title|position|hiring|category|need).*\n?.*'
    job_title = entity_matcher(text, title_list, title_pattern)
    return job_title

#Function to extract Salary

def extract_salary(text):
    pattern = re.compile(r'\b(?:Salary|Compensation|Allowance).*\n?.*',flags=re.I)
    match = re.findall(pattern, text)
    match = re.sub(r"([,\\nr])", "", str(match))

    salary_pattern = re.compile(r'\d+\w?')
    salary = re.findall(salary_pattern, match)

    currency_file = open("currency.txt", encoding="utf-8").read()
    currency_list = eval(currency_file)

    currency = []
    for cur in currency_list:
        if ' '+cur.lower()+' ' in ' '+match.lower()+' ':
            currency.append(cur)

    if  len(salary) == 0:
        salary = "Negotiable"
    elif len(salary) > 1:
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
    location=set()
    location_file = open("location.txt", encoding="utf-8").read()
    location_list = eval(location_file)

    pattern = re.compile(r"(?=(\b" + '\\b|\\b'.join(location_list) + r"\b))", flags=re.I)
    location = re.findall(pattern, text)

    return location

# Function to extract the qualification
def extract_qualification(text):
    text = re.sub('[.|\\n]', '', str(text))
    text = re.sub(r'[^A-Za-z ]', ' ', text)
    text = text.lower()

    degree_list = ['Bachelor', 'Undergraduate', 'Graduate' 'BSC', 'MSC', 'Master', 'Diploma', 'Polytechnic']
    major_list = ['CSE', 'CIS', 'CS', 'EEE', 'ETE', 'Computer', 'BBA']

    degree = []
    major = []
    for deg in degree_list:
        if ' '+deg.lower()+' ' in ' '+text+' ':
            degree.append(deg)
    for maj in major_list:
        if ' '+maj.lower()+' ' in ' '+text+' ':
            major.append(maj)

    return {'degree':degree, 'major':major}


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
    cleaned_text = text_cleaner(text)
    data={"company":extract_company(cleaned_text),
        "title":extract_title(cleaned_text),
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