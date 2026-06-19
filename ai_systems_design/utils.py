import socket


class UtilityMethods:
    @staticmethod
    def read_encoded(file_path):
        with open(file_path, 'rb') as f: return f.read().decode('utf-8')

def create_socket_server(host, port, context):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f'{context} Server listening on {host}:{port}')
    return server_socket

def connect_to_socket_server(host, port, context):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((host, port))
    print(f'Connected to {context} server')
    return server_socket