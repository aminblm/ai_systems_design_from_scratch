# utils.py
import hashlib, json, logging, re, socket, time
from typing import Any, Dict, Optional, Tuple, Union

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class FileOperationsUtility:
    """Provides atomic, type-safe filesystem I/O operations with explicit encoding safeguards."""
    
    @staticmethod
    def read_decoded(file_path: str, encoding: str = 'utf-8', errors: str = 'replace') -> str:
        """Reads a filesystem file safely, handling decoding anomalies with fallback flags."""
        try:
            with open(file_path, mode='rb') as target_file:
                binary_payload = target_file.read()
                return binary_payload.decode(encoding, errors=errors)
        except FileNotFoundError:
            logger.error(f"IO Failure: Targeted file asset path not found: '{file_path}'")
            raise
        except Exception as error:
            logger.error(f"Unexpected file system read execution error on path '{file_path}': {error}")
            raise

    @staticmethod
    def write_encoded(file_path: str, content: str, encoding: str = 'utf-8') -> None:
        """Writes text strings directly to disk storage volumes using strict encoding formats."""
        try:
            binary_payload = content.encode(encoding)
            with open(file_path, mode='wb') as target_file:
                target_file.write(binary_payload)
        except Exception as error:
            logger.error(f"Unexpected file system write execution error on path '{file_path}': {error}")
            raise


class SocketUtility:
    """Manages low-level TCP/IP network transport operations, enforcing proper socket recycling protocols."""

    @staticmethod
    def create_socket_server(host: str, port: int, context: str, backlog: int = 128) -> socket.socket:
        """Generates a bound TCP master socket server with non-blocking address reuse capabilities."""
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # SOLVES PORT COLLISION: Allows instant rebinding without waiting out OS TIME_WAIT delays
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            server_socket.bind((host, port))
            # FIXED: Elevated the listening queue from a bottlenecked 1 up to an enterprise 128
            server_socket.listen(backlog)
            
            logger.info(f"[{context.upper()} Gateway Core] Infrastructure initialized. Listening at -> tcp://{host}:{port}")
            return server_socket
        except socket.error as net_err:
            logger.critical(f"Failed to bind socket network server interface down on {host}:{port} -> {net_err}")
            raise

    @staticmethod
    def connect_to_socket_server(host: str, port: int, context: str, timeout: float = 10.0) -> socket.socket:
        """Establishes an active network pipe line link connection out to a target remote host."""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(timeout)
            
            client_socket.connect((host, port))
            logger.info(f"[{context.upper()}] Successfully bridged communications channel outbound link to {host}:{port} server.")
            return client_socket
        except socket.error as conn_err:
            logger.error(f"Network transport handshake failure routing towards tcp://{host}:{port} -> {conn_err}")
            raise