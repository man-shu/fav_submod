import os
import ast


def count_imports(repo_dir, query):
    import_counts = {}
    for root, _, files in os.walk(repo_dir):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r") as f:
                    try:
                        tree = ast.parse(f.read(), filename=file)
                    except Exception as e:
                        print(f"\nError parsing {os.path.join(root, file)}")
                        print(f"\t{e}")
                        continue
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                if alias.name.startswith(query):
                                    submodules = alias.name.split(".")[1:]
                                    if len(submodules) > 0:
                                        import_counts[submodules[0]] = (
                                            import_counts.get(submodules[0], 0)
                                            + 1
                                        )
                        elif isinstance(node, ast.ImportFrom):
                            if node.module and node.module.startswith(query):
                                submodules = node.module.split(".")[1:]
                                if len(submodules) > 0:
                                    import_counts[submodules[0]] = (
                                        import_counts.get(submodules[0], 0) + 1
                                    )
                                else:
                                    submodules = [
                                        submod.name for submod in node.names
                                    ]
                                    for submodule in submodules:
                                        import_counts[submodule] = (
                                            import_counts.get(submodule, 0) + 1
                                        )
    return import_counts
