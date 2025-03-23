import os
import client.client_data as client_data

def concatenate_files(args):
    try:
        # Ensure a file is provided.
        if len(args) < 2:
            return "No file provided"

        file_path = args[1]

        # Expand user tilde if present.
        file_path = os.path.expanduser(file_path)

        # If the file path is not absolute, resolve it relative to current_directory.
        if not os.path.isabs(file_path):
            current_dir = os.path.expanduser(client_data.current_directory)
            if not os.path.isabs(current_dir):
                current_dir = os.path.abspath(current_dir)
            file_path = os.path.abspath(os.path.join(current_dir, file_path))

        # Open and read the file.
        with open(file_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Failed to cat file."
