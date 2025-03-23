import client.client_data as client_data
import os
import stat
import time


def list_directory(args):
    try:
        # Default flag settings and directory variable
        show_all = False  # for flag 'a'
        long_format = False  # for flag 'l'
        directory = None

        # Process command-line arguments after "ls"
        for arg in args[1:]:
            # If argument starts with '-', treat each character as a flag.
            if arg.startswith("-"):
                for ch in arg[1:]:
                    if ch == 'a':
                        show_all = True
                    elif ch == 'l':
                        long_format = True
            # If the argument is solely composed of flag letters (like "la" or "l")
            elif all(c in "al" for c in arg):
                for ch in arg:
                    if ch == 'a':
                        show_all = True
                    elif ch == 'l':
                        long_format = True
            else:
                # Otherwise, treat the argument as the directory path.
                directory = arg

        # If no directory is specified, use the current directory from client_data.
        if directory is None:
            directory = client_data.current_directory

        # Expand user home and convert to an absolute path.
        directory = os.path.expanduser(directory)
        if not os.path.isabs(directory):
            directory = os.path.abspath(directory)

        # Get the list of files in the directory.
        files = os.listdir(directory)
        if not show_all:
            # Exclude hidden files (those starting with '.')
            files = [f for f in files if not f.startswith('.')]

        # Sort files for consistent output.
        files.sort()

        if long_format:
            # Build a long listing with details for each file.
            lines = []
            for f in files:
                file_path = os.path.join(directory, f)
                try:
                    file_stat = os.stat(file_path)
                    permissions = stat.filemode(file_stat.st_mode)
                    size = file_stat.st_size
                    mtime = time.strftime('%Y-%m-%d %H:%M', time.localtime(file_stat.st_mtime))
                    lines.append(f"{permissions} {size:>8} {mtime} {f}")
                except Exception as e:
                    lines.append(f"?????????? {f}")
            return "\n".join(lines)
        else:
            # Return file names separated by two spaces.
            return "  ".join(files)
    except Exception as e:
        return f"Failed to list directory."
