import socket
import threading



class server:
    def __init__(self) -> None:
        _port = 5000
        _header = 1024
        # Automatically gets the IP address of the computer
        _server = socket.gethostbyname(socket.gethostname())
        _address = (_server, _port)
        _format = "utf-8"

        _client_dict = {
            "": ""
        }

        # There server socket
        _server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _server_socket.bind(_address)

        def handle_client(conn, addr):
            print(f"Client connected from {_address}")

            connected=True
            while connected:
                data = conn.recv(_header).decode(_format)
                if data:
                    msg_len = len(data)
                    msg = conn.recv(msg_len).decode(_format)
                    print(f"{_address} sent packet {data}")
                    if msg == "quit":
                        connected = False
                        print(f"Client disconnected from {addr}")
                    print(f"Received {msg_len} bytes from {addr}")
                    splitmsg = data.split(",")
                    splitmsg[1]
                    print(conn.getpeername()[0])
                    _client_dict[str(conn.getpeername()[0])] = str(splitmsg[0])
                    print(_client_dict[str(conn.getpeername()[0])])
                    print(f"{str(conn.getpeername()[0])} declared target {splitmsg[0]}")
                    
            conn.close()

        def start_server():
            _server_socket.listen()
            print(f"Server started at {_address}")
            while True:
                conn, addr = _server_socket.accept()
                threading.Thread(target=handle_client, args=(conn, addr)).start()
                print(f"[Active Connections] {threading.active_count() -1}")

        print("Starting server...")
        start_server()
server()

