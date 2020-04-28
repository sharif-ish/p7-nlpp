def extract_from_text(text, entity_list):
    for entity in entity_list:
        if entity.lower() in text.lower():
            return entity

def process_text(text):
    processed_text = text.replace('\n', ' ').lower()
    return processed_text

def extract_company_name(text):
    company_file = open("company_name.txt", encoding="utf-8").read()
    company_list_from_api = [i for i in eval(company_file)]
    return extract_from_text(process_text(text), company_list_from_api)

#Summary function( returning all data)
def job_desc_extractor(text):
    text = process_text(text)
    extracted_info = {
        'Company name':extract_company_name(text)
    }
    return extracted_info
