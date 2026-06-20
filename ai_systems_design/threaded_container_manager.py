import json, logging, threading
from socket import socket as Socket
from typing import Dict, Any, List

from ai_systems_design.utils import SocketUtility

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class ThreadedContainerManager:
    """A thread-safe, concurrent TCP daemon for managing mock container environment."""
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

        # Enforce thread-safety since multiple client threads will read/write to memory storage
        self._lock = threading.Lock()
        self.containers: Dict[str, Dict[str, str]] = {}

    def start_server(self):
        """Launch the master connection listener loop."""
        server_socket = SocketUtility.create_socket_server(self.host, self.port, 'Container Manager')
        logger.info(f"Container Daemon initialized safely on {self.host}:{self.port}")
        
        try:
            while True:
                # Accept connections without blocking the execution process of other active sockets
                client_sock, client_address = server_socket.accept()
                logger.info(f'Accepted inbound TCP transaction pipeline from: {client_address}')
                
                
                # Offload client to dedicated execution worker threads
                client_thread = threading.Thread(
                    target=self._worker_thread_entry,
                    args=(client_sock, client_address),
                    daemon=True
                )
                client_thread.start()
        except KeyboardInterrupt:
            logger.info("Shutdown sequence initiated by local supervisor signal.")
        finally:
            server_socket.close()

    def _worker_thread_entry(self, client_sock: Socket, client_address: Any) -> None:
        """Wrapper method to enforce strict structural cleanup using deterministic try-finally guards."""
        try:
            self.handle_client_session(client_sock)
        except Exception as err:
            logger.error(f"Uncaught exception handling transactions for {client_address}: {err}")
        finally:
          logger.info(f"Closing communication pipeline cleanly for: {client_address}")
          client_sock.close()    

    def handle_client_session(self, client_sock: Socket, max_buffer_size: int = 4096) -> None:
        """Processes transactional command lines sequentially for an isolated client socket thread."""
        while True:
            raw_data = client_sock.recv(max_buffer_size)
            if not raw_data: 
                break # Client exited or socket dropped cleanly

            payload = raw_data.decode('utf-8').strip()
            if not payload:
                continue

            logger.info(f'Processing command sequence stream: {payload}')
            parts = payload.split()
            command = parts[0]

            if command in ("exit", "quit"): 
                break

            response = self._route_command(command, parts[1:])
            client_sock.send_all(f"{response}\n".encode('utf-8'))

    def _route_command(self, command: str, args: List[str]) -> str:
            """Routes and executes operations under thread-safe atomic transaction wrappers."""
            match command:
                case 'run': 
                    if not args: 
                        return "ERROR: Usage requires specifying <container_name>"
                    return self._execute_run(container_name=args[0])
                case 'stop': 
                    if not args: 
                        return "ERROR: Usage requires specifying <container_name>"
                    return self._execute_stop(container_name=args[0])
                case 'list': 
                    return self._execute_list()
                case _: 
                    return f"Error: System operation request token '{command}' not recognized."

    def _execute_run(self, container_name: str) -> str:
        with self._lock: # Mutual exclusion lock avoids corruption during concurrent creates
            if container_name in self.containers:
                return f"WARNING: Target container context '{container_name}' already exists."

            mock_file_path = f"/tmp/{container_name}.txt"
            self.containers[container_name] = {
                'status': 'created',
                'file': mock_file_path
            }
            return f"SUCCESS: Container '{container_name}' instanciated at target path '{mock_file_path}'"
        
    def _execute_stop(self, container_name: str) -> str:
        with self._lock:
            if container_name not in self.containers:
                return f"ERROR: Target entity context '{container_name}' could not be located."

            self.containers[container_name]['status'] = 'stopped'
            return f"SUCCESS: Target container allocation instance '{container_name}' stopped."

    def _execute_list(self) -> str:
        with self._lock:
            # Map structural components safely to a clean, decoupled JSON transport structure
            return json.dumps(self.containers)
   