import requests
from config import JOB_LIST_API, API_KEY
HEADER = {'api-key': API_KEY}
respone = requests.get(JOB_LIST_API, headers=HEADER).json()


