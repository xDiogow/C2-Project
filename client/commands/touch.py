import os

from client import client_data


def touch(args):
    """
    Create empty files.
    Usage: touch file1 [file2 ...]
    """
    if len(args) < 2:
        return "Usage: touch file1 [file2 ...]"

    try:
        current = os.path.expanduser(client_data.current_directory)
        results = []

        for path in args[1:]:
            full_path = path if os.path.isabs(path) else os.path.join(current, path)
            full_path = os.path.abspath(full_path)

            with open(full_path, 'a'):
                os.utime(full_path, None)
            results.append(f"Created/updated '{path}'")

        return "\n".join(results)
    except Exception as e:
        return "Failed to create file."