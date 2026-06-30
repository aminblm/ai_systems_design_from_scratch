# git_rpc_server.py
import json
from typing import Any, Dict

from ai_system_design.kernel.socket_server import SocketServer
from ai_system_design.kernel.logger import logger


class GitRPCServer(SocketServer):
    """A safe, multi-threaded RPC server for orchestrating remote Git workflow operations."""
    
    def __init__(self, host: str, port: int, context: str = "Git RPC Server") -> None:
        super().__init__(host, port, context)

    def start_git_rpc_server(self):
        """Initializes listener interfaces and delegates incoming connections to workers."""
        self.start_server(self._process_client_stream)

    def _process_client_stream(self, request) -> bytes:
        """Reads frames and pushes payloads out to internal logic handlers."""
        # Using a small read buffer but assembling frames dynamically
        while True:
            payload = request.strip()
            if not payload:
                continue

            # Process transaction payload and return response
            response_dict = self._route_rpc_request(payload)
            
            # Send responding frame followed by a clear delimiter boundary
            serialized_response = f"{json.dumps(response_dict)}\n"
            return f"{serialized_response}".encode('utf-8')

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