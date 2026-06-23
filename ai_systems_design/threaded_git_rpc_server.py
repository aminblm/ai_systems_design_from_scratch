# threaded_git_rpc_server.py
import json, logging, threading
from socket import socket as Socket
from typing import Any, Dict, Tuple

from ai_systems_design.utils import SocketUtility

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class ThreadedGitRPCServer:
    """A safe, multi-threaded RPC server for orchestrating remote Git workflow operations."""
    
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    def start_server(self):
        """Initializes listener interfaces and delegates incoming connections to workers."""
        server_socket = SocketUtility.create_socket_server(self.host, self.port, "Git Server")
        logger.info(f"Git RPC Server successfully running on {self.host}:{self.port}")
        try:
            while True: 
                client_sock, client_addr = server_socket.accept()
                logger.info(f"Established connection pipeline with client: {client_addr}")

                # Offload task to worker thread to prevent Head-of-Line blocking
                worker = threading.Thread(
                    target=self._connection_worker_lifecycle,
                    args=(client_sock, client_addr),
                    daemon=True
                )
                worker.start()
        except KeyboardInterrupt: 
            logger.info("Server shutting down gracefully via system interrupt signal.")
        finally:
            server_socket.close()

    def _connection_worker_lifecycle(self, client_sock: Socket, client_addr: Tuple[str, int]) -> None:
        """Manages the network transport boundary loop safely for an isolated connection."""
        client_sock.settimeout(15.0)  # Stop dead clients from hanging open permanently
        try:
            self._process_client_stream(client_sock)
        except Exception as err:
            logger.error(f"Error handling transactions for client {client_addr}: {err}")
        finally:
            logger.info(f"Dismantling communication pipeline cleanly for: {client_addr}")
            client_sock.close()

    def _process_client_stream(self, client_sock: Socket) -> None:
        """Reads frames and pushes payloads out to internal logic handlers."""
        # Using a small read buffer but assembling frames dynamically
        while True:
            raw_bytes = client_sock.recv(4096)
            if not raw_bytes:
                break  # Client closed connection cleanly

            payload = raw_bytes.decode('utf-8').strip()
            if not payload:
                continue

            # Process transaction payload and return response
            response_dict = self._route_rpc_request(payload)
            
            # Send responding frame followed by a clear delimiter boundary
            serialized_response = f"{json.dumps(response_dict)}\n"
            client_sock.sendall(serialized_frame := serialized_response.encode('utf-8'))

    def _route_rpc_request(self, raw_payload: str) -> Dict[str, Any]:
        """Parses json strings and handles business logic routing defensively."""
        try:
            request_data = json.loads(raw_payload)
        except json.JSONDecodeError:
            return {"status": "error", "message": "Malformed application framing. Invalid JSON structure."}
        
        # Validate base command schema properties
        if request_data.get("type") != "git" or "command" not in request_data:
            return {"status": "error", "message": "Unsupported orchestration task request type criteria."}
        
        full_command_str = request_data["command"]
        parts = full_command_str.strip().split()

        if not parts or parts[0] != "git":
            return {"status": "error", "message": "Command syntax validation fault: Must begin with 'git'."}
        
        # Abstract router logic replacing static code blocks
        action = parts[1] if len(parts) > 1 else None

        match action:
            case "clone":
                if len(parts) < 3:
                    return {"status": "error", "message": "Syntax validation error: Usage requires 'git clone <url>'"}
                target_repo = parts[2]
                return {
                    "type": "git",
                    "command": "clone",
                    "args": [target_repo],
                    "status": "success",
                    "message": f"Successfully executed system clone task for repository: '{target_repo}'"
                }
            case _:
                return {"status": "error", "message": f"Action routing handler token '{action}' is unmapped."}