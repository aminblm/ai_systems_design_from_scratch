# socket_client.py
from types import TracebackType
from typing import Optional, Type, Any
import socket 

from ai_system_design.logger import logger


class SocketClient:
    """A defensive wrapper around client-side sockets ensuring deterministic lifecycle cleanup."""

    def __init__(self, host: str, port: int, context: str = "Client Socket", timeout_seconds: float = 10.0) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout_seconds
        self.context = context
        self._socket = None

    def connect_to_socket_server(self, timeout: float = 10.0) -> socket.socket:
        """Establishes an active network pipe line link connection out to a target remote host."""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(timeout)
            
            client_socket.connect((self.host, self.port))
            logger.info(f"[{self.context.upper()}] Successfully bridged communications channel outbound link to {self.host}:{self.port} server.")
            return client_socket
        except socket.error as conn_err:
            logger.error(f"Network transport handshake failure routing towards tcp://{self.host}:{self.port} -> {conn_err}")
            raise

    def __enter__(self) -> Any:
        """Establishes the connection when entering a context manager block."""
        try:
            logger.info(f"Establishing connection to {self.host}:{self.port}...")
            self._socket = self.connect_to_socket_server()
            self._socket.settimeout(self.timeout)
            return self
        except Exception as err:
            logger.error(f"Failed to connect to server backend: {err}")
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
                logger.info("Dismantling low-level TCP connection channels cleanly...")
                self._socket.close()
            except Exception as err:
                logger.debug(f"Silent ignore during interface termination: {err}")
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
                logger.warning("Remote host has closed the connection stream channel.")
                return ""
            
            return raw_bytes.decode('utf-8').strip()
        except TimeoutError:
            logger.error("Socket read operation timed out waiting for server response.")
            raise
        except Exception as err:
            logger.error(f"Network error reading transaction line payload: {err}")
            raise

    def send_message(self, message: str) -> None:
        """Transmits a raw payload strings safely out to the established network interface."""
        if not self._socket:
            raise RuntimeError("Cannot write to an uninitialized or dead socket connection.")
        
        if not message.strip():
            logger.warning("Skipping empty message body transmission event.")
            return
        
        try:
            # sendall blocks and continue puping chunks until the entire payload is drained
            self._socket.sendall(message.encode('utf-8'))
            logger.info("Payload successfully flushed down-channel.")
        except Exception as err:
            logger.error(f"Failed sending outbound message package stream: {err}")
            raise