import json

from ai_systems_design.utils import SocketUtility


class GitClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_client(self):
        client_socket = SocketUtility.connect_to_socket_server(self.host, self.port, "Git Client")

        command = "git clone https://github.com/user/repo.git"
        client_socket.sendall(json.dumps({"type": "git", "command": command}).encode())

        response = client_socket.recv(1024).decode()
        print(f"Server response: {response}")

        client_socket.close()

if __name__ == '__main__':
    git_client = GitClient('127.0.0.1', 8080)
    git_client.start_client()