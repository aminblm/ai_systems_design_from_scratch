# container_manager_client.py
import sys
from typing import Optional

from ai_system_design.kernel.socket_client import SocketClient
from ai_system_design.kernel.loggable_mixin import LoggableMixin
from ai_system_design.kernel.test_mixin import TestMixin


class TestContainerManagerClient(TestMixin):
    """Test the container_manager_client module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("ContainerManagerClient initialized.")

    def test_container_manager_client(self):
        # TODO - TEST FAIL - ContainerManager
        # cmd> run
        # Enter container name: python
        # 2026-06-26 05:14:26,834 [WARNING] Remote host has closed the connection stream channel.
        # [Server Response]:
        # Container Management
        
        SERVER_HOST = "127.0.0.1"
        CONTAINER_MANAGER_PORT = 8082
        # Context manager auto-manages low-level cleanup on teardown or crash
        try:
            with ContainerManagerClient(SERVER_HOST, CONTAINER_MANAGER_PORT) as client:
                client.start_interface()
        except Exception as fatal_err:
            self.logger.critical(f"Failed to run service management shell: {fatal_err}")
        

class ContainerManagerClient(SocketClient, LoggableMixin):
    """A clean, defencive CLI client for interacting with a remote container management service."""
    def __init__(self, host: str, port: int) -> None:
        super().__init__(host, port)
        self.logger.info("ContainerManagerClient initialized.")

    def __enter__(self) -> ContainerManagerClient:
        self.context = "Container Manager Client"
        return super().__enter__()
    
    def _send_and_receive(self, payload: str, max_buffer_size: int = 4096) -> str:
        """Helper to safely dispatch requests and await server acknowledgement frames."""
        if not self._socket:
            raise RuntimeError("Cannot write to an uninitialized or dead socket connection.")
        
        if not payload.strip():
            self.logger.warning("Skipping empty message body transmission event.")
            
        response_bytes = self._socket.recv(max_buffer_size)
        if not response_bytes:
            # A zero-byte read indivates the remote server performed a graceful shutdown
            self.logger.warning("Remote host has closed the connection stream channel.")
            return ""
        
        return response_bytes.decode('utf-8').strip()
        
    def _prompt_container_name(self) -> Optional[str]:
        """Collects and validates targeted resource descriptors."""
        print("Enter container name: ", end="", flush=True)
        name = sys.stdin.readline().strip()
        if not name:
            print("❌ Validation Error: Container target name cannot be empty.")
            return None
        return name

    def start_interface(self) -> None:
        """Runs the interactive application event loop."""
        print("\n=== Container Management CLI Platform ===")
        print("Available Commands: [run] [stop] [list] [exit]")

        while True:
            try:
                print("\ncmd> ", end="", flush=True)
                command = sys.stdin.readline().strip().lower()

                if command in ("exit", "quit"):
                    # Gracefully alert daemon we are breaking the socket connection
                    if self._socket:
                        self._socket.sendall("exit".encode('utf-8'))
                    print("Goodbye.")
                    break

                match command:
                    case "run" | "stop":
                        target = self._prompt_container_name()
                        if target:
                            server_response = self._send_and_receive(f"{command} {target}")
                            print(f"[Server Response]: {server_response}")

                    case "list":
                        server_response = self._send_and_receive("list")
                        print(f"[Active Containers]:\n{server_response}")

                    case "":
                        continue

                    case _:
                        print(f"❌ Unknown internal command: '{command}'. Try run, stop, list, or exit.")
            
            except (KeyboardInterrupt, SystemExit):
                print("\nSession aborted via user signal.")
            except Exception as err:
                self.logger.error(f"Network communication cycle faulted: {err}")
                break