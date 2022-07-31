import socket
import threading
import time
import sys, os

class server:
    def __init__(self):
        _port = 5000
        _header = 512
        # Automatically gets the IP address of the computer
        _server = socket.gethostbyname(socket.gethostname())
        _address = (_server, _port)
        _format = "utf-8"

        _client_dict = {
            "": ""
        }
        _clients = []

        # There server socket
        _server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _server_socket.bind(_address)

        def handle_client(conn, addr):
            print(f"Client connected from {_address}")

            connected=True

            while connected:
                if(conn == None):
                    connected = False
                    pass
                #_client_dict[conn] = addr
                _clients.append(conn)
                data = conn.recv(_header).decode(_format)
                if data:
                    conn.sendall(f"ServerKeepAlive,Time:{time.localtime}".encode())
                    msg_len = len(data)
                    print(f"{_address} sent packet {data}")
                    print(f"Received {msg_len} bytes from {addr}")
                    splitmsg = data.split(",")
                    #if(splitmsg[0] == conn):
                    #    break
                    print(conn.getpeername()[0])
                    _client_dict[str(conn.getpeername()[0])] = str(splitmsg[0])
                    print(_client_dict[str(conn.getpeername()[0])])
                    print(f"{str(conn.getpeername()[0])} declared target {splitmsg[0]}")
                    for client in _clients:
                        print(str(client))
                        if(str(client).find(splitmsg[0]) >= 0):
                            client.sendall(str(splitmsg[1]).encode())
                            print(f"{splitmsg[0], client, splitmsg[1]}")
                            connected = False
                            return
                        return
                    conn.close()
                    start_server()
                    return
                else:
                    conn.sendall(f"ServerKeepAlive,Time:{time.localtime}".encode())
            _clients.pop(conn.fileno())
            print(f"{conn.fileno()} disconnected")
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