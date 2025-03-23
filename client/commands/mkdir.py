import os
from client import client_data

def make_directory(args):
    """
    Create directories.
    Usage: mkdir dir1 [dir2 ...]
    """
    if len(args) < 2:
        return "Usage: mkdir dir1 [dir2 ...]"

    try:
        current = os.path.expanduser(client_data.current_directory)
        results = []

        for path in args[1:]:
            # Handle both absolute and relative paths
            full_path = path if os.path.isabs(path) else os.path.join(current, path)
            full_path = os.path.abspath(full_path)

            if os.path.exists(full_path):
                results.append(f"Cannot create '{path}': File exists")
            else:
                os.makedirs(full_path)
                results.append(f"Created directory '{path}'")

        return "\n".join(results)
    except Exception as e:
        return "Failed to create directory."