from searcher import read_token_from_file, search_repositories
from cloner import clone_repository
from analyser import count_imports
import os
from tqdm import tqdm
import json
import sys

# get the query from the first argument
if len(sys.argv) < 2:
    print("Please provide a query.")
    exit()
query = sys.argv[1]

token_file_path = "token"
token = read_token_from_file(token_file_path)
if os.path.exists(f"{query}_repos.json"):
    print(f"Repos already found and saved in {query}_repos.json.\n")
    print(f"Reading repositories from {query}_repos.json...\n")
    with open(f"{query}_repos.json", "r") as file:
        repos = json.load(file)
else:
    print("Searching for repositories...\n")
    repos = search_repositories(query, token)
# find repos whose owner is the query
repos_owned_by_query = []
for repo in repos:
    if repo["owner"]["login"] == query:
        repos_owned_by_query.append(repo)
print(f"Found {len(repos_owned_by_query)} repositories owned by '{query}'.\n")
print(
    f"Removing repositories owned by the {query} from the list of "
    "repositories...\n"
)
# remove repos owned by query from the list of repos
for repo in repos_owned_by_query:
    repos.remove(repo)
print(f"Remaining repositories: {len(repos)}\n")

# find repos larger than 1GB
repos_larger_than_1gb = []
for repo in repos:
    if (repo["size"] / 1024) / 1024 > 1:
        repos_larger_than_1gb.append(repo)

print(f"Found {len(repos_owned_by_query)} repositories owned by '{query}'.\n")
print(
    f"Removing repositories larger than 1GB from the list of "
    "repositories...\n"
)
# remove repos owned by query from the list of repos
for repo in repos_larger_than_1gb:
    repos.remove(repo)
print(f"Remaining repositories: {len(repos)}\n")

os.makedirs("repos", exist_ok=True)
cloned_repos = os.listdir("./repos")
if len(cloned_repos) > 0:
    print(f"{len(cloned_repos)} repositories already cloned.\n")
    print("Do you want to clone them again? (yes/no)")
    response = input()
    if response.lower() != "yes":
        repos = [repo for repo in repos if repo["name"] not in cloned_repos]
        print(f"Repos not cloned yet repositories: {len(repos)}\n")
        print("Cloning them...\n")
        for repo in tqdm(repos):
            clone_repository(repo["clone_url"], f"./repos/{repo['name']}")
else:
    print("No repositories cloned yet.\n")
    print("Calculating the total size of the repositories...\n")
    total_size = sum([repo["size"] for repo in repos])
    print(f"Total size of the repositories: {(total_size / 1024) / 1024} GB\n")
    print("Do you want to clone all the repositories? (yes/no)")
    response = input()
    if response.lower() != "yes":
        print(
            "Do you want to clone a specific number of repositories? "
            "(yes / no (all)  / abort (exit))\n"
        )
        response = input()
        if response.lower() == "yes":
            print("Enter the number of repositories you want to clone:\n")
            num_repos = int(input())
            repos = repos[:num_repos]
        elif response.lower() == "no":
            print("Cloning all repositories...\n")
        elif response.lower() == "abort":
            print("Exiting...\n")
            exit()
    for repo in tqdm(repos):
        clone_repository(repo["clone_url"], f"./repos/{repo['name']}")

print("Analyzing imports...\n")
all_import_counts = {}
for repo in cloned_repos:
    repo_dir = os.path.join("./repos", repo)
    repo_import_counts = count_imports(repo_dir)
    for submodule, count in repo_import_counts.items():
        all_import_counts[submodule] = (
            all_import_counts.get(submodule, 0) + count
        )

print("\nAnalysis complete.\n")
most_used_submodule = max(all_import_counts, key=all_import_counts.get)
print(
    f"\nThe most used submodule is {most_used_submodule} with "
    f"{all_import_counts[most_used_submodule]} imports."
)
print("\nThe order is:")
sorted_import_counts = dict(
    sorted(all_import_counts.items(), key=lambda item: item[1], reverse=True)
)
for submodule, count in sorted_import_counts.items():
    print(f"{submodule}: {count}")
