import socket
import json

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8029))
    print("Conencted to the Git Server")    

    # Example: git clone https://github.com/user/repo.git
    command = "git clone https://github.com/user/repo.git"
    client_socket.sendall(json.dumps({"type": "git", "command": command}).encode())

    response = client_socket.recv(1024).decode()
    print(f"Server response: {response}")

    client_socket.close()

if __name__ == '__main__':
    start_client()