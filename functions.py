import re
import datefinder
from from_external_api import custom_skills
from urlextract import URLExtract
from difflib import SequenceMatcher
from config import matching_ratio
from constant_data import *

# Function to replace new line with space
def new_line_remover(text):
    text = re.sub('[\n\r]', ' ', str(text))
    return text

# Function to remove punctuation and convert to lower case
def text_cleaner(text):
    cleaned = re.sub('[-)(#$%*~:,?_+=@.]',' ',text)
    cleaned = cleaned.lower()
    return cleaned

# Function to match pattern
def pattern_matcher(text, pattern):
    compiled_pattern = re.compile(pattern, flags=re.I)
    match = re.findall(compiled_pattern, text)
    match = " ".join(match)
    text = re.sub('[\n\r]',' ', str(match))
    return text

# Function to search strings within text
def string_searcher(text, string_list):
    matched_strings = []
    for string in string_list:
        if ' '+string.lower()+' ' in ' '+text+' ':
            matched_strings.append(string)
    return matched_strings

# Function to remove punctuation and convert to lower case
def entity_matcher(text, entity_list, pattern):
    text = re.sub('[\n\r]',' ', str(text))
    matched_entities = string_searcher(text, entity_list)
    if len(matched_entities) == 1:
        matched_entity = matched_entities[0]
    elif len(matched_entities) == 0:
        matched_entity = "Not Found"
    else :
        text = pattern_matcher(text, pattern)
        ent = string_searcher(text, entity_list)
        matched_entity = ", ".join(ent)
    return matched_entity

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

#Function to extract Company Name
def extract_company(text):
    company_file = open("company_name.txt", encoding="utf-8").read()  # Company Name file
    company_list =[extra_word_remover(i) for i in eval(company_file)]
    company_name_pattern = r'.*\b(?:company|looking for|is an|is a|is hiring).*\n?.*'
    company_name = entity_matcher(text, company_list, company_name_pattern)
    return company_name

#Function to extract title
def extract_title(text):
    title_file = open("title.txt")  # Title file
    title_list = [line.strip('\n') for line in title_file.readlines()]
    title_pattern = r'.*\b(?:looking for|searching for|title|position|hiring|category|need).*\n?.*'
    job_title = entity_matcher(text, title_list, title_pattern)
    return job_title

# Function to extract Salary text
def salary_text(text):
    text = re.sub('[)(#$%*~:,?_+=@.]', '', text)
    text = text.lower()
    salary_text_pattern = r'\b(?:Salary|Compensation|Allowance).*\n?.*'
    matched_text = pattern_matcher(text, salary_text_pattern)
    return matched_text

# Function to extract Salary
def salary_extractor(text):
    matched_text = salary_text(text)
    salary_pattern = r'(\d+) *(.*) *[-|to] *(\d+) *(.*)'
    matched_salary = re.findall(salary_pattern, matched_text)
    if len(matched_salary) != 0 :
        matched_salary = matched_salary[0]
        digits =[]
        unit = 1
        for s in matched_salary:
            if s.isdigit():
                digits.append(int(s))
            if s.strip() == 'k' or s == 'thousands':
                unit = 1000

        salary = {'min': min(digits)*unit, 'max': max(digits)*unit}
    else:
        digit_and_unit = re.findall(r'(\d+) *([k|thousands])*', matched_text)
        if len(digit_and_unit) != 0:
            digit_and_unit = digit_and_unit[0]
            if digit_and_unit[1].strip() == 'k' or digit_and_unit[1].strip() == 'thousands':
                salary = int(digit_and_unit[0])*1000
            else:
                salary = int(digit_and_unit[0])
        else:
            salary = "Negotiable"
    return salary

# Function to extract salary
def extract_salary(text):
    salary = salary_extractor(text)
    if not isinstance(salary, dict):
        salary = salary
    else:
        salary = ""
    return salary

# Function to extract minimum salary
def extract_minimum_salary(text):
    salary = salary_extractor(text)
    if isinstance(salary, dict):
        salary_min = salary['min']
    else:
        salary_min = ""
    return salary_min

# Function to extract maximum salary
def extract_maximum_salary(text):
    salary = salary_extractor(text)
    if isinstance(salary, dict):
        salary_max = salary['max']
    else:
        salary_max = ""
    return salary_max


# Function to extract currency
def extract_currency(text):
    currency_file = open("currency.txt", encoding="utf-8").read()
    currency_list = eval(currency_file)
    matched_text = salary_text(text)
    currency = string_searcher(matched_text, set(currency_list))
    if len(currency) != 0:
        currency = currency[0]
    else:
        currency = "Not Found"
    return currency


#Function to extract Email
def extract_email(text):
    email_pattern = "[A-Za-z0-9\.\-+_]+@[A-Za-z0-9\.\-+_]+\.[A-Za-z]+"
    email = pattern_matcher(text, email_pattern).replace(' ', ', ')
    return email

#Function to extract Urls
def extract_url(text):
    url = URLExtract().find_urls(text)
    return ", ".join(url)

# Function to extract the vacancy
def extract_vacancy(text):
    vacancy_pattern=r'.*vacanc.*\n?.*'
    match = pattern_matcher(text, vacancy_pattern)
    vacancy = re.findall(r'\d+'," ".join(match))
    if len(vacancy) ==1 :
        vacancy = int(vacancy[0])
    else :
        vacancy = 0
    return vacancy


#Function for extracting skills
def extract_skill(text):
    skills = string_searcher(text, custom_skills)
    return ", ".join(skills)

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
    location_file = open("location.txt", encoding="utf-8").read()
    location_list = eval(location_file)
    location_pattern = r"(?=(\b" + '\\b|\\b'.join(location_list) + r"\b))"
    location = pattern_matcher(text, location_pattern)
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

    return f'{", ".join(degree)} in {", ".join(major)}'


# Function to search a specific string from list within the text
def binary_entity_searcher(text, str_list, default, other):
    text = new_line_remover(text)
    string = string_searcher(text, str_list)
    if len(string) == 0:
        string = default
    else:
        string = other
    return string

# Function to extract the job nature
def extract_job_nature(text):
    default_job_nature = 'Full time'
    other_job_nature = 'Part time'
    job_nature = binary_entity_searcher(text, JOB_NATURES, default_job_nature, other_job_nature)
    return job_nature

# Function to extract the job type
def extract_job_site(text):
    default_job_site = 'On-site'
    other_job_site = 'Remote'
    job_site = binary_entity_searcher(text, JOB_SITES, default_job_site, other_job_site)
    return job_site

# Function to extract the job type
def extract_job_type(text):
    default_job_type = 'Permanent'
    other_job_type = 'Contractual'
    job_type = binary_entity_searcher(text, JOB_TYPES, default_job_type, other_job_type)
    return job_type

def job_desc_extractor(text):
    cleaned_text = text_cleaner(text)
    data={"company":extract_company(cleaned_text),
        "title":extract_title(cleaned_text),
         "salary":extract_salary(text),
         "salary_min":extract_minimum_salary(text),
         "salary_max":extract_maximum_salary(text),
          "currency":extract_currency(cleaned_text),
          "email":extract_email(text),
          "url":extract_url(text),
          "vacancy":extract_vacancy(cleaned_text),
          "skills":extract_skill(cleaned_text),
          "experience":extract_experience(text),
          "deadline":extract_deadline(text),
          "location":extract_location(text),
          "qualification":extract_qualification(cleaned_text),
          "job_nature":extract_job_nature(cleaned_text),
          "job_site":extract_job_site(cleaned_text),
          "job_type":extract_job_type(cleaned_text)
          }
    return data