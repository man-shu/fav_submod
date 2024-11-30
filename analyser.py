import os
import ast

def count_imports(repo_dir):
    import_counts = {}
    for root, _, files in os.walk(repo_dir):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r") as f:
                    tree = ast.parse(f.read(), filename=file)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                if alias.name.startswith("nilearn"):
                                    import_counts[alias.name] = import_counts.get(alias.name, 0) + 1
                        elif isinstance(node, ast.ImportFrom):
                            if node.module and node.module.startswith("nilearn"):
                                import_counts[node.module] = import_counts.get(node.module, 0) + 1
    return import_counts

# Example usage
all_import_counts = {}
for repo in os.listdir("./repos"):
    repo_dir = os.path.join("./repos", repo)
    repo_import_counts = count_imports(repo_dir)
    for module, count in repo_import_counts.items():
        all_import_counts[module] = all_import_counts.get(module, 0) + count

most_used_submodule = max(all_import_counts, key=all_import_counts.get)
print(f"The most used submodule is {most_used_submodule} with {all_import_counts[most_used_submodule]} imports.")