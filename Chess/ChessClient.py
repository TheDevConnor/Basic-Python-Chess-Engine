import socket

_header = 512  
_disconnect = "quit"
_port = 5000
_server = "10.0.0.101"
_address = (_server, _port)
uinput = ["", "", "", ""]


def message(message):
    print(message)
    _client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _client_socket.connect(_address)
    _client_socket.sendall(message.encode())
    data = _client_socket.recv(_header).decode()
    print(data)
    while True:
        print("hi")
        _client_socket.sendall(message.encode())
        data = _client_socket.recv(_header).decode()
        print(data)
        if data:
            print(data)
            _client_socket.sendall(message.encode())
            _client_socket.close()
            return data
        else:
            _client_socket.sendall(message.encode())
            return data
