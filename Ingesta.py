import requests
import time
import math
from urllib.parse import parse_qs, urlparse
from pymongo import MongoClient

COMM_LIMIT = 5000

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
# pabloUsername = "PabloBlazquezSanchez"
# pabloToken = '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'
# pabloClient_id = '32bfc97d07c905811c12'
# pabloClient_Secret = '047d8902e71e977fd711f9706bf0a6d95bc0d473'

headers = {'Authorization': 'Bearer '+token, 'Accept': 'application/vnd.github+json'}

# MONGODB_HOST = f'mongodb+srv://{usernameMongo}:{passwordMongo}@cluster0.fus1bnz.mongodb.net/'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DB_NAME = 'github'
COLLECTION_COMMITS = 'commits'
connection= MongoClient(MONGODB_HOST, MONGODB_PORT)
collCommits= connection[DB_NAME][COLLECTION_COMMITS]
repos_url= 'https://api.github.com/repos/{}/{}/commits?since=2019-01-01&page={}&per_page={}'
rate_url = 'https://api.github.com/rate_limit'
user= 'sourcegraph'
project= 'sourcegraph'
max_pages = math.ceil((get_commits_count(owner_name=user, repo_name=project)/100))

for page in range (1+max_pages): #range tiene de intervalo [0,range-1]
    query= {'client_id': client_id, 'client_secret': client_secret}
    rate_limit = requests.get(rate_url, params=query, headers=headers).json()['resources']['core']
    print(rate_limit)
    if rate_limit['remaining'] > 0:
        # CONSULTA
        url= repos_url.format(user, project, page, 100)
        commits = requests.get(url, params=query, headers=headers)
        commits_dict = commits.json()
        for commit in commits_dict:
            commit['projectId'] = project
            # print(str(commit))
            collCommits.insert_one(commit)
    else:
        delta = (rate_limit['reset']-time.time())/1000
        time.sleep(delta)








































'''
import requests
import pymongo
from datetime import datetime

# Configuración de MongoDB
MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
MONGO_DB_NAME = "github_commits"
MONGO_COLLECTION_NAME = "commits"

# Configuración de GitHub
GITHUB_API_BASE_URL = "https://api.github.com/"
GITHUB_REPO_OWNER = "sourcegraph"
GITHUB_REPO_NAME = "sourcegraph"
GITHUB_AUTH_TOKEN = "your_github_auth_token"  # Reemplaza con tu token de autenticación de GitHub

# Función para obtener commits desde GitHub
def get_commits():
    headers = {
        "Authorization": f"token {GITHUB_AUTH_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"{GITHUB_API_BASE_URL}repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/commits"
    params = {
        "since": "2019-01-01T00:00:00Z",
        "per_page": 100
    }
    commits = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            new_commits = response.json()
            if not new_commits:
                break
            commits.extend(new_commits)
            if "Link" in response.headers:
                links = response.headers["Link"].split(",")
                for link in links:
                    if 'rel="next"' in link:
                        url = link.split(";")[0].strip("<>")
                        break
            else:
                break
        else:
            print("Error al obtener commits:", response.status_code)
            break

    return commits

# Función para obtener detalles de un commit desde GitHub
def get_commit_details(commit_sha):
    headers = {
        "Authorization": f"token {GITHUB_AUTH_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"{GITHUB_API_BASE_URL}repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/commits/{commit_sha}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener detalles del commit {commit_sha}: {response.status_code}")
        return None

# Función para insertar commits en MongoDB
def insert_commits_into_mongodb(commits):
    client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_NAME]
    for commit in commits:
        commit_details = get_commit_details(commit['sha'])
        if commit_details:
            extended_info = {
                "files_modified": [file['filename'] for file in commit_details['files']],
                "changes_stats": commit_details['stats']
            }
            commit.update(extended_info)
            collection.insert_one(commit)
    client.close()

if __name__ == "__main__":
    commits = get_commits()
    insert_commits_into_mongodb(commits)

'''





'''
import requests
import pymongo
import time
from datetime import datetime

# Configuración de MongoDB
MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
MONGO_DB_NAME = "github_commits"
MONGO_COLLECTION_NAME = "commits"

# Configuración de GitHub
GITHUB_API_BASE_URL = "https://api.github.com/"
GITHUB_REPO_OWNER = "sourcegraph"
GITHUB_REPO_NAME = "sourcegraph"
GITHUB_AUTH_TOKEN = "your_github_auth_token"  # Reemplaza con tu token de autenticación de GitHub

# Función para obtener commits desde GitHub
def get_commits():
    headers = {
        "Authorization": f"token {GITHUB_AUTH_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"{GITHUB_API_BASE_URL}repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/commits"
    params = {
        "since": "2019-01-01T00:00:00Z",
        "per_page": 100
    }
    commits = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            new_commits = response.json()
            if not new_commits:
                break
            commits.extend(new_commits)
            if "Link" in response.headers:
                links = response.headers["Link"].split(",")
                for link in links:
                    if 'rel="next"' in link:
                        url = link.split(";")[0].strip("<>")
                        break
            else:
                break
            # Comprobación del límite de velocidad
            remaining_requests = int(response.headers["X-RateLimit-Remaining"])
            if remaining_requests <= 1:  # Si queda solo una solicitud, esperar un minuto
                reset_time = int(response.headers["X-RateLimit-Reset"])
                sleep_time = max(0, reset_time - time.time()) + 1
                print(f"Esperando {sleep_time} segundos para evitar alcanzar el límite de velocidad de GitHub...")
                time.sleep(sleep_time)
        else:
            print("Error al obtener commits:", response.status_code)
            break

    return commits

# Función para obtener detalles de un commit desde GitHub
def get_commit_details(commit_sha):
    headers = {
        "Authorization": f"token {GITHUB_AUTH_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"{GITHUB_API_BASE_URL}repos/{GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}/commits/{commit_sha}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener detalles del commit {commit_sha}: {response.status_code}")
        return None

# Función para insertar commits en MongoDB
def insert_commits_into_mongodb(commits):
    client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_NAME]
    for commit in commits:
        commit_details = get_commit_details(commit['sha'])
        if commit_details:
            extended_info = {
                "files_modified": [file['filename'] for file in commit_details['files']],
                "changes_stats": commit_details['stats']
            }
            commit.update(extended_info)
            collection.insert_one(commit)
    client.close()

if __name__ == "__main__":
    commits = get_commits()
    insert_commits_into_mongodb(commits)

'''