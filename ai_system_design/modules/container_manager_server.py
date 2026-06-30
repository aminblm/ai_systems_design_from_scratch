# container_manager_server.py
import json, threading
from typing import Dict, List

from ai_system_design.kernel.socket_server import SocketServer
from ai_system_design.kernel.logger import logger


class ContainerManagerServer(SocketServer):
    """A thread-safe, concurrent TCP daemon for managing mock container environment."""
    def __init__(self, host: str, port: int, context: str = "Container Manager") -> None:
        super().__init__(host, port, context)

        # Enforce thread-safety since multiple client threads will read/write to memory storage
        self._lock = threading.Lock()
        self.containers: Dict[str, Dict[str, str]] = {}

    def start_container_manager_server(self):
        """Launch the master connection listener loop."""
        self.start_server(self.handle_client_session) 

    def handle_client_session(self, request: str) -> bytes:
        """Processes transactional command lines sequentially for an isolated client socket thread."""
        while True:
            payload = request.strip()
            if not payload:
                continue

            logger.info(f'Processing command sequence stream: {payload}')
            parts = payload.split()
            command = parts[0]

            if command in ("exit", "quit"): 
                return b"Exiting..."

            response = self._route_command(command, parts[1:])
            return f"{response}\n".encode('utf-8')

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
   