# resilient_git_rpc_client.py
import json, logging
from types import TracebackType
from typing import Optional, Type, Dict, Any

from ai_systems_design.utils import SocketUtility

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class ResilientGitRPCClient:
    """A resilient Remote Procedure Call (RPC) client for conveying Git tasks over safe TCP frames."""

    def __init__(self, host: str, port: int, timeout_seconds: float = 30.0) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout_seconds
        self._socket = None

    def __enter__(self) -> ResilientGitRPCClient:
        """Context initialization establishing active transport channels."""
        try:
            logger.info(f"Connecting to remote orchestration pipeline worker on {self.host}:{self.port}...")
            self._socket = SocketUtility.connect_to_socket_server(self.host, self.port, "Git Client")
            self._socket.settimeout(self.timeout)
            return self
        except Exception as err:
            logger.error(f"Failed establishing TCP handshake socket initialization path: {err}")
            self.close()
            raise

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ) -> None:
        self.close()

    def _send_frame(self, payload_dict: Dict[str, Any]) -> None:
        """Serializes payload to JSON and transmits it with a clear newline delimiter boundary."""
        if not self._socket:
            raise RuntimeError("Cannot communicate over a disconnected network socket pipeline.")

        # Adding a trailing newline character provides a clear frame marker for the server's buffer reader
        serialized_frame = f"{json.dumps(payload_dict)}\n"
        self._socket.sendall(serialized_frame.encode('utf-8'))

    def _receive_frame(self, max_bytes: int = 4096) -> str:
        """Awaits data bytes returning cleanly formatted feedback strings."""
        if not self._socket:
            raise RuntimeError("Cannot read over a disconnected network socket pipeline.")
        
        data = self._socket.recv(max_bytes)
        if not data:
            raise ConnectionAbortedError("Remote coordination daemon severed communication channels abruptly.")
            
        return data.decode('utf-8').strip()

    def dispatch_clone(self, repository_url: str) -> str:
        """Sends a dynamic repository target out for evaluation execution."""
        if not repository_url.startswith(("http://", "https://", "git@", "ssh://")):
            raise ValueError(f"Target argument payload fails basic syntax layout rules: {repository_url}")
        
        payload = {
            "type": "git",
            "command": f"git clone {repository_url}"
        }

        try:
            logger.info(f"Dispatching clone target transaction payload details for: {repository_url}")
            self._send_frame(payload)
            
            # Wait for execution response
            response = self._receive_frame()
            return response
        except Exception as err:
            logger.error(f"Failed to execute target payload exchange pattern: {err}")
            raise

    def close(self) -> None:
        if self._socket:
            try:
                self._socket.close()
            except Exception:
                pass
            finally:
                self._socket = None
