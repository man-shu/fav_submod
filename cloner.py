import os
import subprocess


def clone_repository(repo_url, clone_dir):
    subprocess.run(["git", "clone", repo_url, clone_dir])
