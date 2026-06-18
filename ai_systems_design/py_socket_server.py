import socket
import json 

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8028))
    server_socket.listen(1)
    print('Socket server listening on port 8028...')

    while True: 
        client_socket, addr = server_socket.accept()
        print(f'Connection from {addr}')

        message = "Hey What's up?"

        client_socket.sendall(message.encode())

        response = client_socket.recv(1024).decode()
        print(response)

        client_socket.close()

if __name__ == '__main__':
    start_server()