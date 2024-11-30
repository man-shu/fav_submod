from searcher import read_token_from_file, search_repositories
from cloner import clone_repository
from analyser import count_imports
import os

print("Searching for repositories...\n")
token_file_path = "token"
token = read_token_from_file(token_file_path)
query = "nilearn"
repos = search_repositories(query, token)
print(f"Found {repos['total_count']} repositories for query '{query}'.\n")

print("Cloning repositories...\n")
os.makedirs("repos", exist_ok=True)
for repo in repos["items"]:
    clone_repository(repo["clone_url"], f"./repos/{repo['name']}")

print("Analyzing imports...\n")
all_import_counts = {}
for repo in os.listdir("./repos"):
    repo_dir = os.path.join("./repos", repo)
    repo_import_counts = count_imports(repo_dir)
    for module, count in repo_import_counts.items():
        all_import_counts[module] = all_import_counts.get(module, 0) + count
most_used_submodule = max(all_import_counts, key=all_import_counts.get)

print(
    f"The most used submodule is {most_used_submodule} with "
    f"{all_import_counts[most_used_submodule]} imports."
)
