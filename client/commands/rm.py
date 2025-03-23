import os
import shutil
from client import client_data

def remove(args):
    """
    Remove files or directories.
    Usage: rm [-r] path1 [path2 ...]
    -r: recursively remove directories and their contents
    """
    if len(args) < 2:
        return "Usage: rm [-r] path1 [path2 ...]"

    recursive = False
    paths = []

    # Parse arguments
    for arg in args[1:]:
        if arg == "-r":
            recursive = True
        else:
            paths.append(arg)

    if not paths:
        return "No path specified"

    try:
        current = os.path.expanduser(client_data.current_directory)
        results = []

        for path in paths:
            # Handle both absolute and relative paths
            full_path = path if os.path.isabs(path) else os.path.join(current, path)
            full_path = os.path.abspath(full_path)

            if os.path.exists(full_path):
                if os.path.isdir(full_path):
                    if recursive:
                        shutil.rmtree(full_path)
                        results.append(f"Removed directory '{path}'")
                    else:
                        results.append(f"Cannot remove '{path}': Is a directory")
                else:
                    os.remove(full_path)
                    results.append(f"Removed '{path}'")
            else:
                results.append(f"Cannot remove '{path}': No such file or directory")

        return "\n".join(results)
    except Exception as e:
        return f"Failed to remove."