import requests

def search_repositories(query, token):
    url = f"https://api.github.com/search/repositories?q={query}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Example usage
token = "your_github_token"
query = "nilearn"
repos = search_repositories(query, token)