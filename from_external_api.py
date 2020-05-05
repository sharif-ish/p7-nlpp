import requests
from config import SKILL_LIST_API, API_KEY
import time

HEADER = {'api-key': API_KEY}

def api_response_to_list(url, key):
    respone = requests.get(url, headers=HEADER).json()
    item_list = []
    for res in respone:
        item_list.append(res[key])
    return item_list


# Get skills from API
custom_skills = api_response_to_list(SKILL_LIST_API, 'name')
'''

# Company API
start = time.time()
company_name = api_response_to_list(COMPANY_API, 'name')
end = time.time()

print("Time to get data from company API:", end-start)
#print(custom_skills)
#print(len(custom_skills))
#print(company_name)
#print(len(company_name))


filename = "company_name.txt"
try:
    file_company_name = open(filename,"w")
    file_company_name.write(str(company_name))
    file_company_name.close()
    print(f"Data save to {filename}")
except Exception as e:
    print(e)


'''
