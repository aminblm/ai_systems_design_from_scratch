# resilient_client_socket.py
import logging, sys
from types import TracebackType
from typing import Optional, Type
from ai_systems_design.utils import SocketUtility

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class ResilientClientSocket:
    """A defensive wrapper around client-side sockets ensuring deterministic lifecycle cleanup."""
    def __init__(self, host: str, port: int, timeout_seconds: float = 10.0) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout_seconds
        self._socket = None

    def __enter__(self) -> ResilientClientSocket:
        """Establishes the connection when entering a context manager block."""
        try:
            logger.info(f"Establishing connection to {self.host}:{self.port}...")
            self._socket = SocketUtility.connect_to_socket_server(
                self.host, self.port, "Client Socket"
            )
            self._socket.settimeout(self.timeout)
            return self
        except Exception as err:
            logger.error(f"Failed to connect to server backend: {err}")
            self.close()
            raise

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        """Guarantees socket closure regardless of internal loop exceptions."""
        self.close()
        #returning None or False lets any bubbling runtime exceptions propagate normally
        return False
    
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