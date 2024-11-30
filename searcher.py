import requests
import json


def search_repositories(query, token, max_pages=100):
    repos = []
    for page in range(1, max_pages + 1):
        url = f"https://api.github.com/search/repositories?q={query}&page={page}&per_page=100"
        headers = {"Authorization": f"token {token}"}
        response = requests.get(url, headers=headers).json()
        total_count = response["total_count"]
        repos.extend(response["items"])
        if total_count == len(repos):
            break
    # write the repos to a file
    output_file = f"{query}_repos.json"
    with open(output_file, "w") as file:
        json.dump
    return repos


def read_token_from_file(file_path):
    with open(file_path, "r") as file:
        token = file.read().strip()
    return token
