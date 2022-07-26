import socket

_disconnect = "quit"
_port = 5000
_server = "10.0.0.101"
_address = (_server, _port)
uinput = ["", "", "", ""]

class ChessClient():
    def __init__(self) -> None:
        global _client_socket
        global _established



    def send_message(self, message, _isEstablished):
        _client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _isEstablished = True
        _client_socket.connect(_address)
        _client_socket.send(message.encode())
        print(f"Sent {message}")
        return _isEstablished


    def receive_message(self, _isEstablished):
        if _isEstablished != True:
            _client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _client_socket.connect(_address)
            data = _client_socket.recv(2048).decode()
            print(f"Received {data}")
            return data
        else:
            _client_socket.connect(_address)
            data = _client_socket.recv(2048).decode()
            print(f"Received {data}")
            return data