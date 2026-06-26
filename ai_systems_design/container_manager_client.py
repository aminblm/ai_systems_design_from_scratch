# container_manager_client.py
import sys
from typing import Optional

from ai_systems_design.socket_client import SocketClient
from ai_systems_design import logger


class ContainerManagerClient(SocketClient):
    """A clean, defencive CLI client for interacting with a remote container management service."""

    def __enter__(self) -> ContainerManagerClient:
        self.context = "Container Manager Client"
        return super().__enter__()
    
    def _send_and_receive(self, payload: str, max_buffer_size: int = 4096) -> str:
        """Helper to safely dispatch requests and await server acknowledgement frames."""
        if not self._socket:
            raise RuntimeError("Cannot write to an uninitialized or dead socket connection.")
        
        if not payload.strip():
            logger.warning("Skipping empty message body transmission event.")
            
        response_bytes = self._socket.recv(max_buffer_size)
        if not response_bytes:
            # A zero-byte read indivates the remote server performed a graceful shutdown
            logger.warning("Remote host has closed the connection stream channel.")
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
                logger.error(f"Network communication cycle faulted: {err}")
                break
    
    def close(self) -> None:
        """Idempotently flushes and dismantles low-level kernel descriptors."""
        if self._socket:
            try:
                logger.info("Dismantling low-level TCP connection channels cleanly...")
                self._socket.close()
            except Exception as err:
                logger.debug(f"Silent ignore during interface termination: {err}")
            finally:
                self._socket = None