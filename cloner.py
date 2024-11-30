import os
import subprocess

def clone_repository(repo_url, clone_dir):
    subprocess.run(["git", "clone", repo_url, clone_dir])

# Example usage
for repo in repos['items']:
    clone_repository(repo['clone_url'], f"./repos/{repo['name']}")