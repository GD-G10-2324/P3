import requests
from urllib.parse import parse_qs, urlparse

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

print(get_commits_count(owner_name='sourcegraph',repo_name='sourcegraph'))