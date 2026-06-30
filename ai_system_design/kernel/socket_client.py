# socket_client.py
import socket, sys 
from types import TracebackType
from typing import Optional, Type, Any

from ai_system_design.kernel.loggable_mixin import LoggableMixin
from ai_system_design.kernel.test_mixin import TestMixin


class TestSocketClient(TestMixin):
    """Test the socket_client module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestSocketClient initialized.")
    
    def test_socket_client(self):
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


class SocketClient(LoggableMixin):
    """A defensive wrapper around client-side sockets ensuring deterministic lifecycle cleanup."""

    def __init__(self, host: str, port: int, context: str = "Client Socket", timeout_seconds: float = 10.0) -> None:
        super().__init__()
        self.host = host
        self.port = port
        self.timeout = timeout_seconds
        self.context = context
        self._socket = None
        self.logger.info("SocketClient initialized.")

    def connect_to_socket_server(self, timeout: float = 10.0) -> socket.socket:
        """Establishes an active network pipe line link connection out to a target remote host."""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(timeout)
            
            client_socket.connect((self.host, self.port))
            self.logger.info(f"[{self.context.upper()}] Successfully bridged communications channel outbound link to {self.host}:{self.port} server.")
            return client_socket
        except socket.error as conn_err:
            self.logger.error(f"Network transport handshake failure routing towards tcp://{self.host}:{self.port} -> {conn_err}")
            raise

    def __enter__(self) -> Any:
        """Establishes the connection when entering a context manager block."""
        try:
            self.logger.info(f"Establishing connection to {self.host}:{self.port}...")
            self._socket = self.connect_to_socket_server()
            self._socket.settimeout(self.timeout)
            return self
        except Exception as err:
            self.logger.error(f"Failed to connect to server backend: {err}")
            if self._socket:
                self._socket.close()
            raise

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        """Guarantees socket closure regardless of internal loop exceptions."""
        if self._socket:
            self._socket.close()
            #returning None or False lets any bubbling runtime exceptions propagate normally
            return False
    
    def close(self) -> None:
        """Idempotently flushes and dismantles low-level kernel descriptors."""
        if self._socket:
            try:
                self.logger.info("Dismantling low-level TCP connection channels cleanly...")
                self._socket.close()
            except Exception as err:
                self.logger.debug(f"Silent ignore during interface termination: {err}")
            finally:
                self._socket = None
    
    def receive_message(self, max_buffer_size: int = 4096) -> str:
        """Safely reads inbound streams from the remote host buffer."""
        if not self._socket:
            raise RuntimeError("Cannot read from an uninitialized or dead socket connection.")
        
        try:
            raw_bytes = self._socket.recv(max_buffer_size)
            if not raw_bytes:
                # A zero-byte read indivates the remote server performed a graceful shutdown
                self.logger.warning("Remote host has closed the connection stream channel.")
                return ""
            
            return raw_bytes.decode('utf-8').strip()
        except TimeoutError:
            self.logger.error("Socket read operation timed out waiting for server response.")
            raise
        except Exception as err:
            self.logger.error(f"Network error reading transaction line payload: {err}")
            raise

    def send_message(self, message: str) -> None:
        """Transmits a raw payload strings safely out to the established network interface."""
        if not self._socket:
            raise RuntimeError("Cannot write to an uninitialized or dead socket connection.")
        
        if not message.strip():
            self.logger.warning("Skipping empty message body transmission event.")
            return
        
        try:
            # sendall blocks and continue puping chunks until the entire payload is drained
            self._socket.sendall(message.encode('utf-8'))
            self.logger.info("Payload successfully flushed down-channel.")
        except Exception as err:
            self.logger.error(f"Failed sending outbound message package stream: {err}")
            raise