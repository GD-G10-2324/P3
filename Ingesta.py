import requests
import time
import math
import os
from urllib.parse import parse_qs, urlparse
from pymongo import MongoClient
from dotenv import load_dotenv

COMM_LIMIT = 5000
load_dotenv()

def get_commits_count(owner_name: str, repo_name: str) -> int:
    """
    Returns the number of commits to a GitHub repository.
    """
    rurl = 'https://api.github.com/repos/{}/{}/commits?since=2019-01-01&per_page=1'
    url= rurl.format(owner_name, repo_name)
    r = requests.get(url)
    links = r.links
    rel_last_link_url = urlparse(links["last"]["url"])
    rel_last_link_url_args = parse_qs(rel_last_link_url.query)
    rel_last_link_url_page_arg = rel_last_link_url_args["page"][0]
    commits_count = int(rel_last_link_url_page_arg)
    return commits_count

token = os.getenv('TOKEN')
client_id = os.getenv('CLIENTID')
client_secret = os.getenv('CLIENTSECRET')

headers = {'Authorization': 'Bearer '+token, 'Accept': 'application/vnd.github+json'}
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'github'
COLLECTION_COMMITS = 'commits'
connection= MongoClient(MONGODB_HOST, MONGODB_PORT)
collCommits= connection[DB_NAME][COLLECTION_COMMITS]
repos_url= 'https://api.github.com/repos/{}/{}/commits?since=2019-01-01&page={}&per_page={}'
commit_url='https://api.github.com/repos/{}/{}/commits/{}'
rate_url = 'https://api.github.com/rate_limit'
user= 'sourcegraph'
project= 'sourcegraph'
max_pages = math.ceil((get_commits_count(owner_name=user, repo_name=project)/100))

for page in range (1+max_pages): #range tiene de intervalo [0,range-1]
    query= {'client_id': client_id, 'client_secret': client_secret}
    rate_limit = requests.get(rate_url, params=query, headers=headers).json()['resources']['core']
    print(rate_limit)
    if rate_limit['remaining'] > 0:
        # CONSULTA DE TODOS LOS COMMITS DE 100 EN 100
        url= repos_url.format(user, project, page, 100)
        commits = requests.get(url, params=query, headers=headers)
        commits_dict = commits.json()
        for commit in commits_dict:
            rate_limit = requests.get(rate_url, params=query, headers=headers).json()['resources']['core']
            if rate_limit['remaining'] <= 0:
                delta = (rate_limit['reset']-time.time())/1000
                time.sleep(delta)

            #CONSULTA INDIVIDUAL DE CADA COMMIT
            commitProperties_url = commit_url.format(user, project, commit['sha'])
            commitSpecs = requests.get(commitProperties_url, params=query, headers=headers).json()
            
            file_list = []

            for file in commitSpecs['files']:
                if file['status']  == 'modified':
                    file_list.append(file) 

            #ALMACENADO EN LA BASE DE DATOS
            commit['projectId'] = project
            commit['stats'] = commitSpecs['stats']
            commit['files'] = file_list

            collCommits.insert_one(commit)
    else:
        delta = (rate_limit['reset']-time.time())/1000
        time.sleep(delta)
