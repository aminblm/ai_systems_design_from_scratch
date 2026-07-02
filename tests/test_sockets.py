# test_sockets.py

import ai_system_design.kernel.sockets as sockets
from ai_system_design.kernel.mixins import TestMixin

class TestSockets(TestMixin):
    def __init__(self):
        super().__init__()
    
    def test(self):
        super().test()
        # Create a socket
        socket = sockets.Socket(sockets.ADDRESS_FAMILY_INET, sockets.SOCKET_STREAM)
        # Connect to a server
        server_address = (("localhost", 8080))
        socket.connect(server_address)
        # Send data
        message = b"Hello Server!"
        socket.sendall(message)
        # Receive data
        data = socket.receive(4096)
        self.logger.info(f"Received: {data}")
        # Close the connection
        socket.close()
