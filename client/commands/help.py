# Add this function to client/commands/help.py
def get_help(args):
    """
    Display available commands and their descriptions.
    Usage: help
    """
    return "\n".join([
        "Available commands:",
        "ls - List directory contents",
        "cd - Change the current directory",
        "pwd - Print the current working directory",
        "cat - Concatenate and display file contents",
        "rm - Remove files or directories",
        "rmdir - Remove empty directories",
        "mkdir - Create directories",
        "touch - Create empty files",
        "echo - Display a line of text",
        "help - Display this help message"
        "exit/disconnect/quit - Disconnect from the client"
    ])
