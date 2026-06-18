import socket
import json 

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8028))

    response = client_socket.recv(1024).decode()
    print(response)

    print("Send a message:")
    message = input()
    client_socket.sendall(message.encode())
    
    client_socket.close()

if __name__ == '__main__':
    start_client()