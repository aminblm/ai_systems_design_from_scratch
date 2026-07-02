# test_socket_server.py

from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.kernel.socket_server import SocketServer


class TestSocketServer(TestMixin):
    """Test the socket_server module functionality."""

    def __init__(self) -> None:
        """TestSocketServer Constructor."""
        super().__init__()

    async def test(self):
        """TestSocketServer Test."""
        super().test()
        SERVER_HOST = "127.0.0.1"
        SOCKET_SERVER_PORT = 8080

        server = SocketServer(SERVER_HOST, SOCKET_SERVER_PORT)

        server.add_middleware(lambda text: f"Middleware: {text}".encode("utf-8"))
        server.add_middleware(lambda text: f"Another Middleware: {text}".encode("utf-8"))

        await server.start_socket_server()

