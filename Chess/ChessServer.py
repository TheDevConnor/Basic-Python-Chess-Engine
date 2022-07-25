import socket
import threading

_port = 5000
# Automatically gets the IP address of the computer
_server = socket.gethostbyname(socket.gethostname())
_address = (_server, _port)
_format = "utf-8"

# There server socket
_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_server_socket.bind(_address)

def handle_client(conn, addr):
    print(f"Client connected from {_address}")

    connected=True
    while connected:
        data = conn.recv(1024).decode(_format)
        if data:
            msg_len = len(data)
            msg = conn.recv(msg_len).decode(_format)
            print(f"Received {msg_len} bytes from {addr}")

            if msg == "quit":
                connected = False
                print(f"Client disconnected from {addr}")

            print(f"{_address} > {msg}")
    conn.close()

def start_server():
    _server_socket.listen()
    print(f"Server started at {_address}")
    while True:
        conn, addr = _server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()
        print(f"[Active Connections] {threading.activeCount() -1}")

print("Starting server...")
start_server()