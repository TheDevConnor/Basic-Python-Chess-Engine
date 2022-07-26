import socket

global _client_socket

_disconnect = "quit"
_port = 5000
_server = "35.223.181.160"
_address = (_server, _port)
uinput = ["", "", "", ""]

    
def send_message(message):
    _client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _client_socket.connect(_address)
    _client_socket.send(message.encode())
    print(f"Sent {message}")

        