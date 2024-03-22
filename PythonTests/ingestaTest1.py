import requests
import pymongo
import time
from datetime import datetime

# Configuración de MongoDB
MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
MONGO_DB_NAME = "github"
MONGO_COLLECTION_NAME = "commits"

# Configuración de GitHub
GITHUB_API_BASE_URL = "https://api.github.com/"
GITHUB_REPO_OWNER = "sourcegraph"
GITHUB_REPO_NAME = "sourcegraph"

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