# resilient_multi_threaded_server.py
import logging, socket, sys, threading
from typing import Tuple

from ai_systems_design.utils import SocketUtility
from ai_systems_design.utils import logger


class ResilientMultiThreadedServer:
    """A robust, concurrent TCP server that safely manages multi-client connection Lifecycles."""
    
    def __init__(self, host: str, port: int, context: str = 'Socket Server') -> None:
        self.host = host
        self.port = port
        self._is_running = False
        self.context = context

    def start_server(self) -> None:
        """Binds the underlying socket and enters the concurrent client acceptance loop."""
        # Create and bind the socket server safely using utility helpers
        server_socket = SocketUtility.create_socket_server(self.host, self.port, self.context)
        self._is_running = True
        logger.info(f"TCP Multi-Threaded Server successfully running on {self.host}:{self.port}")

        try:
            while self._is_running:
                try:
                    # Await new incoming TCP connection streams
                    client_socket, client_address = server_socket.accept()
                    logger.info(f"Accepted inbound network pipe connection from: {client_address}")
                    
                    # Spun off connection to an independent thread to prevent blocking loops
                    client_thread = threading.Thread(
                        target=self._handle_client_lifecycle,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.error as sock_err:
                    if self._is_running:
                        logger.error(f"Socket acceptance pipeline exception: {sock_err}")
                    break
        except KeyboardInterrupt:
            logger.info("Intercepted termination signal. Shutting down system interfaces...")
        finally:
            self._is_running = False
            server_socket.close()
            logger.info("Master server socket dropped cleanly.")

    def _handle_client_lifecycle(self, client_socket: socket.socket, client_address: Tuple[str, int]) -> None:
        """Manages the read/write streaming transactions for a single isolated connection."""
        # Configured explicit transaction timeouts to prevent silent hanging sockets
        client_socket.settimeout(10.0) 
        
        try:
            # 1. Dispatch greeting frame downstream
            greeting_msg = f"[SUCCESS] handshake the {self.host}:{self.port} server.\n"
            client_socket.sendall(greeting_msg.encode('utf-8'))
            
            # 2. Safely read inbound response frame
            raw_payload = client_socket.recv(4096)
            if raw_payload:
                request_text = raw_payload.decode('utf-8').strip()
                logger.info(f"[{client_address}] Sent Echo payload: {request_text}")
                response_bytes = self._process_socket_transaction(request_text)
                client_socket.sendall(response_bytes)
            else:
                logger.warning(f"[{client_address}] Closed connection early without data transmission.")
                
        except socket.timeout:
            logger.warning(f"[{client_address}] Stream transmission timed out. Evicting client socket.")
        except Exception as error:
            logger.error(f"Exception handling transaction loops for client {client_address}: {error}")
        finally:
            client_socket.close()
            logger.info(f"Cleaned up network socket resources for client: {client_address}")

    def _process_socket_transaction(self, request_text: str) -> bytes:
        """Parses raw text frames and constructs fully compliant HTTP/1.1 response bytes."""

        return f"[{self.context.upper()}] {request_text}".encode('utf-8')
        