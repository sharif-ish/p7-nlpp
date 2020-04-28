import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from from_external_api import custom_skills
porterStemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')

#data preprocessing
def data_preprocess(text):
    srt=nltk.sent_tokenize(text) #Removing punctuation mark
    word_list=[]
    lkt=[]
    for i in range(len(srt)):
        wordd=tokenizer.tokenize(srt[i]) #word tokenization
        for n in range(3,0,-1):
            lst=list(nltk.ngrams(wordd,n)) #ngrams must be alist
            word_list=[' '.join(w) for w in lst] #converting the list of tuples to string
            lkt.append(word_list)
    flat_list=[i for item in lkt for i in item] #Converting the lists of list to a list
    return flat_list

# Function to extract the title
def title_extract(text):
    srt = nltk.sent_tokenize(text)  # Removing punctuation mark
    word_list = []
    lkt = []
    for i in range(len(srt)):
        wordd = tokenizer.tokenize(srt[i])  # word tokenization
        for n in range(3, 0, -1):
            lst = list(nltk.ngrams(wordd, n))  # ngrams must be alist
            word_list = [' '.join(w) for w in lst]  # converting the list of tuples to string
            lkt.append(word_list)
    flat_list = [i for item in lkt for i in item]  # Converting the lists of list to a list
    title_file = open("TITLE.txt")  # Title file
    title_lst = [line.strip('\n').lower() for line in title_file.readlines()]  # Coverting the title file to list
    title_lst = [porterStemmer.stem(word) for word in title_lst]  # Steemimg the title list
    for f in flat_list:
        if porterStemmer.stem(f.lower()) in title_lst:  # stemming the ngrams and comaparing with the title list
            return f
            break

# Function to extract the Company name
def company_name_extract(text):
    srt = nltk.sent_tokenize(text)
    srt = srt[:3]
    word_list = []
    lkt = []
    for i in range(len(srt)):
        wordd = tokenizer.tokenize(srt[i])  # word tokenization
        for n in range(5, 0, -1):
            lst = list(nltk.ngrams(wordd, n))  # ngrams must be alist
            word_list = [' '.join(w) for w in lst]  # converting the list of tuples to string
            lkt.append(word_list)
    flat_list = [i for item in lkt for i in item]  # Converting the lists of list to a list
    company_list = set()
    company_file = open("company_name.txt", encoding="utf-8").read()
    company_list_from_api = [i.strip().lower().replace('.','').replace(' ','') for i in eval(company_file)]
    for f in flat_list:
        if f.lower() in company_list_from_api:
            company_list.add(f.lower())
            return company_list

#Function to extract the salary
def salary_extract(text):
    pattern=re.compile(r'\b(?:Sa|Co)\w* ?[A-Za-z]* ?:? ?[A-Za-z]*.? ?\b(?:\d+[A-Za-z]*,?\d* ?-? ?[A-Za-z]* ?\d+[A-Za-z]*,?\d*|Ne\w*)')
    match=re.findall(pattern,text)
    return match
#Function to extract the Company email address
def email_extract(text):
    pattern=re.compile(r'\S+@\S+')
    match=re.findall(pattern,text)
    return match

#Function to extract the Company location
def location_extract(text):
    flat_list=data_preprocess(text)
    loc=set()
    file=open("location.txt").readlines()
    file_lst=[line.split(',') for line in file]
    fillle=[k for f in file_lst for k in f]
    len(fillle)

    for f in flat_list:
        if f.lower() in fillle:
            loc.add(f)
    return loc


# Function to extract the skill
def skill_extract(text):
    flat_list = data_preprocess(text)
    skill_list = set()
    cleaned_skills = []
    for skill in custom_skills:
        cleaned_skills.append(skill.strip().lower().replace('.', ''))
    for f in flat_list:
        if f.lower() in cleaned_skills:
            skill_list.add(f.lower())
    return skill_list

# Function to extract the qualification
def extract_qualification(text):
    pattern = re.compile(r'Ed\w+ ?\w+.*\n?\S.*')
    match = re.findall(pattern, text)
    matchh = re.sub(r'\\n', ' ', str(match))
    pattern = re.sub('[^A-Za-z ]', "", str(matchh))
    qulification_list = ['bsc', 'msc', 'masters', 'diploma', 'Polytechnic']
    dept_name = ['cse', 'cis', 'csse', 'eee', 'computer application', 'computer', 'computer science']
    word = nltk.word_tokenize(pattern)
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
#Function for extracting experience
def extract_experience(text):
    pattern=re.compile(r'Exp.*\n?.*')
    match=re.findall(pattern,text)
    sub_newline=re.sub(r'\\n',' ',str(match))
    experience=re.findall(r'\d ?-?t?o?\+? ?\d? ?\S+',str(sub_newline))
    if len(experience)>0:
        return experience[0]
    else:
        return experience

#Summary function( returning all data)
def job_desc_extractor(text):
    data={"Title":title_extract(text),
         "Company Name":company_name_extract(text),
         "Salary":salary_extract(text),
         "Email":email_extract(text),
         "Location":location_extract(text),
         "Skills":skill_extract(text),
         "Qualification":extract_qualification(text),
         "Experience":extract_experience(text)}
    return data