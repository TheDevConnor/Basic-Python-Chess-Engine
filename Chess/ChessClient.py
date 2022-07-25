import socket

_disconnect = "quit"
_port = 5000
_server = "10.0.0.101"
_address = (_server, _port)

#The client socket
_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_client_socket.connect(_address)

def send_message(message):
    _client_socket.send(message.encode())
    print(f"Sent {message}")

send_message("Hello World!")
input("Press Enter to continue...")
send_message("Hello World!")
input("Press Enter to continue...")
send_message("Hello World!")
input("Press Enter to continue...")

send_message(_disconnect)