from client import client_data
import os

def change_directory(args):
    if len(args) < 2:
        return "Usage: cd <directory>"

    new_directory = args[1]
    current = os.path.expanduser(client_data.current_directory)

    try:
        # Handle both absolute and relative paths
        if os.path.isabs(new_directory):
            directory = new_directory
        else:
            directory = os.path.abspath(os.path.join(current, new_directory))


        os.chdir(directory)
        client_data.current_directory = directory

        display_dir = os.path.basename(directory) or directory
        return f"Changed directory to {display_dir}"
    except Exception as e:
        return "Failed to change directory"