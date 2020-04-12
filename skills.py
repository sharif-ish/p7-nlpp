import requests

URL = 'http://p7.ishraak.com/api/skill_list/'
API_KEY = '96d56aceeb9049debeab628ac760aa11'
HEADER = {'api-key': API_KEY}
response = requests.get(URL, headers=HEADER)
skills = response.json()

custom_skills = []
for skill in skills:
    custom_skills.append(skill['name'])