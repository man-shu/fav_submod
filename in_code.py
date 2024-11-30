from searcher import read_token_from_file, search_code
from cloner import clone_repository
from analyser import count_imports
import os
from tqdm import tqdm
import json
import sys

# # get the query from the first argument
# if len(sys.argv) < 2:
#     print("Please provide a query.")
#     exit()
query = "import nilearn OR from nilearn"

token_file_path = "token"
token = read_token_from_file(token_file_path)
if os.path.exists(f"{query}_files.json"):
    print(f"files already found and saved in {query}_files.json.\n")
    print(f"Reading files from {query}_files.json...\n")
    with open(f"{query}_files.json", "r") as file:
        files = json.load(file)
else:
    print("Searching for files...\n")
    files = search_code(query, token)
# find files whose owner is the query
files_owned_by_query = []
for fil in files:
    if fil["repository"]["owner"]["login"] == "nilearn":
        files_owned_by_query.append(fil)
print(f"Found {len(files_owned_by_query)} files owned by nilearn.\n")
print(f"Removing files owned by the nilearn from the list of files...\n")
# remove files owned by query from the list of files
for fil in files_owned_by_query:
    files.remove(fil)
print(f"Remaining files: {len(files)}\n")

# # find files larger than 1GB
# files_larger_than_1gb = []
# for fil in files:
#     if (fil["size"] / 1024) / 1024 > 1:
#         files_larger_than_1gb.append(fil)

# print(f"Found {len(files_larger_than_1gb)} files larger than 1GB.\n")
# print(f"Removing files larger than 1GB from the list of files...\n")
# # remove files owned by query from the list of files
# for fil in files_larger_than_1gb:
#     files.remove(fil)
# print(f"Remaining files: {len(files)}\n")

os.makedirs(f"{query}_files", exist_ok=True)
cloned_files = os.listdir(f"./{query}_files")
if len(cloned_files) > 0:
    print(f"{len(cloned_files)} files already cloned.\n")
    print("Do you want to clone them again? (yes/no)")
    response = input()
    if response.lower() == "yes":
        print("Cloning all files again...\n")
        for fil in tqdm(files):
            clone_url = fil["repository"]["html_url"]
            clone_repository(clone_url, f"./{query}_files/{clone_url}")
    else:
        print("Do you want to clone the remaining files? (yes/no)")
        response = input()
        if response.lower() == "yes":
            files = [fil for fil in files if fil["name"] not in cloned_files]
            print(f"files not cloned yet: {len(files)}\n")
            print("Cloning them...\n")
            for fil in tqdm(files):
                clone_url = fil["repository"]["html_url"]
                clone_repository(clone_url, f"./{query}_files/{clone_url}")
else:
    print("No files cloned yet.\n")
    # print("Calculating the total size of the files...\n")
    # total_size = sum([fil["size"] for fil in files])
    # print(f"Total size of the files: {(total_size / 1024) / 1024} GB\n")
    print("Do you want to clone all the files? (yes/no)")
    response = input()
    if response.lower() != "yes":
        print(
            "Do you want to clone a specific number of files? "
            "(yes / no (all)  / abort (exit))\n"
        )
        response = input()
        if response.lower() == "yes":
            print("Enter the number of files you want to clone:\n")
            num_files = int(input())
            files = files[:num_files]
        elif response.lower() == "no":
            print("Cloning all files...\n")
        elif response.lower() == "abort":
            print("Exiting...\n")
            exit()
    for fil in tqdm(files):
        clone_url = fil["repository"]["html_url"]
        clone_repository(clone_url, f"./{query}_files/{clone_url}")

print("Analyzing imports...\n")
all_import_counts = {}
for fil in cloned_files:
    fil_dir = os.path.join(f"./{query}_files", fil)
    fil_import_counts = count_imports(fil_dir, query)
    for submodule, count in fil_import_counts.items():
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
    print(f"\t{submodule}: {count}")
