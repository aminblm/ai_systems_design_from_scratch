# test_socket_client.py

import sys 

from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.kernel.socket_client import SocketClient


class TestSocketClient(TestMixin):
    """Test the socket_client module functionality."""

    def __init__(self) -> None:
        """TestSocketClient Constructor."""
        super().__init__()
    
    def test(self):
        """TestSocketClient Test."""
        super().test()
        SERVER_HOST = "127.0.0.1"
        SOCKET_SERVER_PORT = 8080
        # Using a context manager completely replaces manual tracking of .close()
        try:
            with SocketClient(SERVER_HOST, SOCKET_SERVER_PORT) as client:
                server_handshake = client.receive_message()
                if server_handshake:
                    print(f"\n[Server]: {server_handshake}")

                #Collect explicit local buffer arguments
                print("\nEnter outound payload message:")
                user_input = sys.stdin.readline().strip()
            
                if user_input:
                    client.send_message(user_input)
                    print(client.receive_message())
        
        except (KeyboardInterrupt, SystemExit):
            self.logger.info("\nExecution cancelled by user signal interrupt. Exiting safely.")
        except Exception as general_failure:
            self.logger.critical(f"Fatal application runtime termination event: {general_failure}")