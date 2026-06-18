import json 

import ai_systems_design.utils as utils


class GitServer:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_server(self):
        server_socket = utils.create_socket_server(self.port, self.host, "Git Server")

        while True: 
            client_socket, addr = server_socket.accept()
            print(f'Connection from {addr}')

            data = client_socket.recv(1024).decode()
            print(f'Received {data}')

            if not data: client_socket.sendall(json.dumps({"error": "No data received"}).encode()); continue

            try:
                response = json.dumps({
                    "type": "git",
                    "command": "clone",
                    "args": ["https://github.com/user/repo.git"],
                    "status": "success",
                    "message": "Cloned repository successfully"
                }).encode()
                client_socket.sendall(response)
            except Exception as e: client_socket.sendall(json.dumps({"error": str(e)}).encode())
            client_socket.close()

if __name__ == '__main__':
    git_server = GitServer('127.0.0.1', 8080)
    git_server.start_server()