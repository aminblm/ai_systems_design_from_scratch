import logging, sys
from types import TracebackType
from typing import Optional, Type
from ai_systems_design.utils import SocketUtility

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class ClientSocket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def connect_client(self):
        client_socket = SocketUtility.connect_to_socket_server(self.host, self.port, "Client Socket")

        response = client_socket.recv(1024).decode()
        print(response)

        print("Send a message:")
        message = input()
        client_socket.sendall(message.encode())
        
        client_socket.close()

if __name__ == '__main__':
    client_socket = ClientSocket('127.0.0.1', 8080)
    client_socket.connect_client()
