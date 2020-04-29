import re

def extract_from_text(text, entity_list):
    for entity in entity_list:
        if entity.lower() in text.lower():
            return entity

def process_text(text):
    processed_text = text.replace('\n', ' ').lower()
    return processed_text

# Company name extraction
def extract_company_name(text):
    company_file = open("company_name.txt", encoding="utf-8").read()
    company_list_from_api = eval(company_file)
    return extract_from_text(text, company_list_from_api)

# Job title extraction
def extract_job_title(text):
    title_file = open("job_titles.txt")
    title_list = [line.strip('\n') for line in title_file.readlines()]  # Coverting the title file to list
    return extract_from_text(text, title_list)

#Email Extraction
def extract_email(text):
    pattern = re.compile(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+")
    email = re.findall(pattern,text)
    return email

#Summary function( returning all data )
def job_desc_extractor(text):
    processed_text = process_text(text)
    extracted_info = {
        'Company Name':extract_company_name(processed_text),
        "Title": extract_job_title(processed_text),
        "Salary": None,
        "Email": extract_email(text),
        "Location": None,
        "Skills": None,
        "Qualification": None,
        "Experience": None
    }
    return extracted_info
