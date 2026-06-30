# git_rpc_client.py
import json
from typing import Dict, Any

from ai_system_design.kernel.socket_client import SocketClient
from ai_system_design.kernel.loggable_mixin import LoggableMixin
from ai_system_design.kernel.test_mixin import TestMixin


class TestGitRPCClient(TestMixin):
    """Test the git_rpc_client module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestGitRPCClient initialized.")

    def test_git_rpc_client(self):
        SERVER_HOST = "127.0.0.1"
        GIT_RPC_SERVER_PORT = 8084
        TARGET_REPO = "https://github.com/aminblm/ai_systems_design_from_scratch.git"

        # Context manager implementation replaces sequential manual channel closes entirely
        try:
            with GitRPCClient(SERVER_HOST, GIT_RPC_SERVER_PORT) as git_agent:
                server_feedback = git_agent.dispatch_clone(repository_url=TARGET_REPO)
                print(f"\n[Execution Worker Response]: {server_feedback}")
                
        except Exception as fatal_error:
            self.logger.critical(f"Abrupt termination handling repository pipeline sequence tasks: {fatal_error}")
        
        
class GitRPCClient(SocketClient, LoggableMixin):
    """A resilient Remote Procedure Call (RPC) client for conveying Git tasks over safe TCP frames."""

    def __init__(self, host: str, port: int) -> None:
        super().__init__(host, port)
        self.logger.info("GitRPCClient initialized.")

    def __enter__(self) -> GitRPCClient:
        self.context = "Git RPC Client"
        return super().__enter__()

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
            self.logger.info(f"Dispatching clone target transaction payload details for: {repository_url}")
            self._send_frame(payload)
            
            # Wait for execution response
            response = self._receive_frame()
            return response
        except Exception as err:
            self.logger.error(f"Failed to execute target payload exchange pattern: {err}")
            raise
