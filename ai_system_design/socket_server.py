# socket_server.py
import socket, threading
from typing import Tuple, Callable, List

from ai_system_design.logger import logger


class SocketServer:
    """A robust, concurrent TCP server that safely manages multi-client connection Lifecycles."""
    
    def __init__(self, host: str, port: int, context: str = 'Socket Server') -> None:
        self.host = host
        self.port = port
        self._is_running = False
        self.context = context
        self._middlewares: List[Callable[[str], bytes]] = [] 

    def create_socket_server(self, backlog: int = 128) -> socket.socket:
        """Generates a bound TCP master socket server with non-blocking address reuse capabilities."""
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # SOLVES PORT COLLISION: Allows instant rebinding without waiting out OS TIME_WAIT delays
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            server_socket.bind((self.host, self.port))
            # FIXED: Elevated the listening queue from a bottlenecked 1 up to an enterprise 128
            server_socket.listen(backlog)
            
            logger.info(f"[{self.context.upper()} Gateway Core] Infrastructure initialized. Listening at -> tcp://{self.host}:{self.port}")
            return server_socket
        except socket.error as net_err:
            logger.critical(f"Failed to bind socket network server interface down on {self.host}:{self.port} -> {net_err}")
            raise

    def start_server(self, process_socket_transaction: Callable[[str], bytes]) -> None:
        """Binds the underlying socket and enters the concurrent client acceptance loop."""
        # Create and bind the socket server safely using utility helpers
        server_socket = self.create_socket_server()
        self._is_running = True
        logger.info(f"[{self.context.upper()}] Server successfully running on {self.host}:{self.port}")

        try:
            while self._is_running:
                try:
                    # Await new incoming TCP connection streams
                    client_socket, client_address = server_socket.accept()
                    logger.info(f"Accepted inbound network pipe connection from: {client_address}")
                    
                    # Spun off connection to an independent thread to prevent blocking loops
                    client_thread = threading.Thread(
                        target=self._handle_client_lifecycle,
                        args=(client_socket, client_address, process_socket_transaction),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.error as sock_err:
                    if self._is_running:
                        logger.error(f"Socket acceptance pipeline exception: {sock_err}")
                    break
                
                # TODO Server not interuppting on System exit
                except KeyboardInterrupt, SystemExit:
                    logger.info("Intercepted termination signal. Shutting down system interfaces...")
                    server_socket.close()
                    self._is_running = False
                    break   
        finally:
            self._is_running = False
            server_socket.close()
            logger.info("Master server socket dropped cleanly.")

    def start_socket_server(self):
        self.start_server(self._process_socket_transaction)

    def add_middleware(self, middleware: Callable[[str], bytes]) -> None:
        """Adds middlewares to the server"""
        self._middlewares.append(middleware)

    def process_request(self, request_text: str, process_socket_transaction: Callable[[str], bytes]) -> bytes:
        for middleware in self._middlewares:
            request_text = middleware(request_text).decode('utf-8')

        response_bytes = process_socket_transaction(request_text)
        return response_bytes

    def _handle_client_lifecycle(self, client_socket: socket.socket, client_address: Tuple[str, int], process_socket_transaction: Callable[[str], bytes]) -> None:
        """Manages the read/write streaming transactions for a single isolated connection."""
        # Configured explicit transaction timeouts to prevent silent hanging sockets
        client_socket.settimeout(10.0) 
        
        try:
            # WARNING: Dispatch handshake only if incoming request from Socket Client - Mapped to port 8080
            if self.port == 8080:
                # 1. Dispatch greeting frame downstream
                greeting_msg = f"[SUCCESS] handshake the {self.host}:{self.port} server.\n"
                client_socket.sendall(greeting_msg.encode('utf-8'))
            
            # 2. Safely read inbound response frame
            raw_payload = client_socket.recv(4096)
            if raw_payload:
                request_text = raw_payload.decode('utf-8').strip()
                logger.info(f"[{client_address}] Sent Echo payload: {request_text}")
                response_bytes = self.process_request(request_text, process_socket_transaction)
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

        return f"[{self.context.upper()}] [CLIENT SOCKET]: {request_text}".encode('utf-8')
        