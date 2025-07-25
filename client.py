import socket
import json

HOST = '127.0.0.1'
PORT = 5000

def send_command(command):
    with socket.create_connection((HOST, PORT)) as sock:
        sock.send(json.dumps(command).encode())
        response = sock.recv(1024)
        print("Response:", json.loads(response.decode()))

if __name__ == "__main__":
    send_command({"type": "PUT", "key": "test", "value": "123"})
    send_command({"type": "GET", "key": "test"})
