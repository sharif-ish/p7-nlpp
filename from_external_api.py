import requests
from config import SKILL_LIST_API, API_KEY, COMPANY_NAME_API
import time

HEADER = {'api-key': API_KEY}

def api_response_to_list(url, key):
    respone = requests.get(url, headers=HEADER).json()
    item_list = []
    for res in respone:
        item_list.append(res[key].lower())
    return item_list

custom_skills = api_response_to_list(SKILL_LIST_API, 'name')

