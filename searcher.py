import requests

def search_repositories(query, token):
    url = f"https://api.github.com/search/repositories?q={query}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def read_token_from_file(file_path):
    with open(file_path, 'r') as file:
        token = file.read().strip()
    return token

# Example usage
token_file_path = "token"
token = read_token_from_file(token_file_path)
query = "nilearn"
repos = search_repositories(query, token)