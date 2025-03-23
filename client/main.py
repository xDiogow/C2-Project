import json
import socket

import client.client_data as client_data
from client.commands.cat import concatenate_files
from client.commands.cd import change_directory
from client.commands.ls import list_directory
from client.commands.pwd import print_working_directory
from client.commands.rm import remove
from client.commands.rmdir import remove_directory
from client.commands.mkdir import make_directory

# Command registry
COMMANDS = {
    "ls": list_directory,
    "cd": change_directory,
    "pwd": print_working_directory,
    "cat": concatenate_files,
    "rm": remove,
    "rmdir": remove_directory,
    "mkdir": make_directory,
}


def execute_command(command_line):
    args = command_line.split()
    if not args:
        return "No command provided"

    command = args[0]
    if command not in COMMANDS:
        return f"Unknown command: {command}"

    return COMMANDS[command](args)

def keep_alive_client(host='127.0.0.1', port=9999):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"[*] Connected to {host}:{port}")

    try:
        while True:
            response = client_socket.recv(10240)
            if not response:
                print("[*] Connection closed by server")
                break

            command = response.decode('utf-8')
            print(f"[*] Received: {command}")

            client_response = execute_command(command)

            data = {
                "response": client_response,
                "current_directory": client_data.current_directory
            }
            print(data)

            client_socket.sendall((json.dumps(data) + "\n").encode('utf-8'))
            response = client_socket.recv(1024)
            print(f"[*] Received: {response.decode('utf-8')}")
    finally:
        client_socket.close()
        print("[*] Connection closed.")


if __name__ == "__main__":
    keep_alive_client()
