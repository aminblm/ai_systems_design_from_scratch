import ai_systems_design.utils as utils

class ServerSocket:
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_server(self):
        server_socket = utils.create_socket_server(self.host, self.port, 'Socket Server')

        while True: 
            client_socket, addr = server_socket.accept()
            print(f'Connection from {addr}')

            message = "Hey What's up?"
            client_socket.sendall(message.encode())

            response = client_socket.recv(1024).decode()
            print(response)

            client_socket.close()

if __name__ == '__main__':
    server_socket = ServerSocket('127.0.0.1', 8080)