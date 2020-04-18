import requests
from config import SKILL_LIST_API, SKILL_LIST_API_KEY

HEADER = {'api-key': SKILL_LIST_API_KEY}
response = requests.get(SKILL_LIST_API, headers=HEADER)
skills = response.json()

custom_skills = []
for skill in skills:
    custom_skills.append(skill['name'])
