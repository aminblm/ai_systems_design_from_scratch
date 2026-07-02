from ai_system_design.kernel._sockets import *
from ai_system_design.kernel.mixins import TestMixin

class TestSockets(TestMixin):
    def __init__(self):
        super().__init__()
    
    def test(self):
        super().test()
        # Create a socket
        socket = Socket(Socket.INET_ADDRESS, Socket.SOCKET_STREAM)
        # Connect to a server
        server_address = (("localhost", 8080))
        socket.connect(server_address)
        # Send data
        message = "Hello Server!"
        socket.sendall(message)
        # Receive data
        data = socket.receive(4096)
        self.logger.info(f"Received: {data}")
        # Close the connection
        socket.close()


class Socket(_sockets.Socket):
    pass

