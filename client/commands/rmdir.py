import os
from client import client_data

def remove_directory(args):
    """
    Remove empty directories.
    Usage: rmdir dir1 [dir2 ...]
    """
    if len(args) < 2:
        return "Usage: rmdir dir1 [dir2 ...]"

    try:
        current = os.path.expanduser(client_data.current_directory)
        results = []

        for path in args[1:]:
            # Handle both absolute and relative paths
            full_path = path if os.path.isabs(path) else os.path.join(current, path)
            full_path = os.path.abspath(full_path)

            if os.path.exists(full_path):
                if os.path.isdir(full_path):
                    if os.listdir(full_path):
                        results.append(f"Failed to remove '{path}': Directory not empty")
                    else:
                        os.rmdir(full_path)
                        results.append(f"Removed directory '{path}'")
                else:
                    results.append(f"Failed to remove '{path}': Not a directory")
            else:
                results.append(f"Failed to remove '{path}': No such directory")

        return "\n".join(results)
    except Exception as e:
        return "Failed to remove directory."