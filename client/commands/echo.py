def echo(args):
    """
    Display a line of text.
    Usage: echo [text ...]
    """
    if len(args) < 2:
        return ""

    # Join all arguments after "echo" with spaces
    return " ".join(args[1:])