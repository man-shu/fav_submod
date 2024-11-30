import requests
import json


def search_code(query, token, max_pages=100):
    files = []
    for page in range(1, max_pages + 1):
        url = f"https://api.github.com/search/code?q={query}+language:python&page={page}&per_page=100"
        headers = {"Authorization": f"token {token}"}
        response = requests.get(url, headers=headers).json()
        try:
            total_count = response["total_count"]
        except KeyError:
            print("Error in response:")
            print(response)
            break
        files.extend(response["items"])
        if total_count == len(files):
            break
    # write the code snippets to a file
    output_file = f"{query}_files.json"
    with open(output_file, "w") as file:
        json.dump(files, file, indent=4)
    return files


def search_repositories(query, token, max_pages=100):
    repos = []
    for page in range(1, max_pages + 1):
        url = f"https://api.github.com/search/repositories?q={query}&page={page}&per_page=100"
        headers = {"Authorization": f"token {token}"}
        response = requests.get(url, headers=headers).json()
        try:
            total_count = response["total_count"]
        except KeyError:
            print("Error in response:")
            print(response)
            break
        repos.extend(response["items"])
        if total_count == len(repos):
            break
    # write the repos to a file
    output_file = f"{query}_repos.json"
    with open(output_file, "w") as file:
        json.dump(repos, file, indent=4)
    return repos


def read_token_from_file(file_path):
    with open(file_path, "r") as file:
        token = file.read().strip()
    return token
