import requests
import time
import pymongo
from urllib.parse import parse_qs, urlparse
from pymongo import MongoClient

COMM_LIMIT = 5000
FAULT_DELTA = 20
SECONDSHOUR = 3600

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

username = "PAULACASTILLEJOBRAVO"
token = "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"
client_id = "3bab62c6318084a0999b"
client_secret = "9d5c1a69fb0c65cf45780164de266f100cd11d3c"
# contraseña atlas
# usernameMongo = 'PAULACASTILLEJOBRAVO'
# passwordMongo = 'KtBpNycnHOlwMwT7'
headers = {'Authorization': 'Bearer '+token, 'Accept': 'application/vnd.github+json'}

# MONGODB_HOST = f'mongodb+srv://{usernameMongo}:{passwordMongo}@cluster0.fus1bnz.mongodb.net/'
# MONGODB_PORT = 27017
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'github'
COLLECTION_COMMITS = 'commits'
connection= MongoClient(MONGODB_HOST, MONGODB_PORT)
collCommits= connection[DB_NAME][COLLECTION_COMMITS]
repos_url= 'https://api.github.com/repos/{}/{}/commits?since=2019-01-01&page={}&per_page={}'
#https://api.github.com/repos/sourcegraph/sourcegraph/commits?since=2019-01-01&page=1&per_page=1

user= 'sourcegraph'
project= 'sourcegraph'
interval = round(SECONDSHOUR/(COMM_LIMIT-FAULT_DELTA),3)
totalcommits = get_commits_count(owner_name=user, repo_name=project)

# while totalcommits >= 0:
url= repos_url.format(user, project, totalcommits, 1)

query= {'client_id': client_id, 'client_secret': client_secret}
r = requests.get(url, params=query, headers=headers)
commits_dict= r.json()
for commit in commits_dict:
    commit['projectId'] = project
    print(str(commit))
    collCommits.insert_one(commit)

time.sleep(interval) 
# totalcommits-=1