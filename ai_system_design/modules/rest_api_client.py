# rest_api_client.py
import sys
from typing import Optional

from ai_system_design.kernel.socket_client import SocketClient
from ai_system_design.kernel.loggable_mixin import LoggableMixin
from ai_system_design.kernel.test_mixin import TestMixin


class TestRESTAPIClient(TestMixin):
    """Test the rest_api_client module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestRESTAPIClient initialized.")

    def test(self):
        super().test()
        SERVER_HOST = "127.0.0.1"
        REST_API_PORT = 8083
        # Context manager pattern ensures explicit teardown safeguards apply uniformly
        try:
            RESTAPIClient(SERVER_HOST, REST_API_PORT).start_repl_loop()
        except Exception as initialization_failure:
            self.logger.critical(f"Failed to engage network testing suite system execution nodes: {initialization_failure}")

        
        
class RESTAPIClient(SocketClient, LoggableMixin):
    """A clean raw-socket HTTP client implementating defensive parsing frames over TCP streams."""

    def init__(self, host: str, port: int) -> None:
        super().__init__(host, port)
        self.logger.info("RESTAPIClient initialized.")

    def __enter__(self) -> RESTAPIClient:
        self.context = "REST API Client"
        return super().__enter__()
    
    def send_http_request(self, method: str, path: str, body: Optional[str] = None) -> None:
        """Constructs and flushes compliant raw HTTP/1.1 text frames down the pipe."""
        if not self._socket:
            raise RuntimeError("Cannot dispatch request over uninitialized or closed socket interface.")
        
        # Ensure correct path formatting structure
        formatted_path = path if path.startswith("/") else f"/{path}"
        
        # Assemble standard HTTP/1.1 message structure layout lines
        request_buffer = [
            f"{method.upper()} {formatted_path} HTTP/1.1",
            f"Host: {self.host}:{self.port}",
            "Connection: keep-alive",
            "Accept: */*"
        ]

        if body:
            # FIXED: Correctly added the mandatory Content-Length header mapping rules
            request_buffer.append("Content-Type: application/json")
            request_buffer.append(f"Content-Length: {len(body.encode('utf-8'))}")
            request_buffer.append("\r\n" + body)
        else:
            # Double trailing markers signifying empty transmission payload termination block
            request_buffer.append("\r\n")

        raw_payload = "\r\n".join(request_buffer)
        self._socket.sendall(raw_payload.encode('utf-8'))
        self.logger.info(f"Successfully flushed raw {method} request downstream.")

    def receive_and_parse_response(self) -> None:
        """Reads incoming network streams and outputs clear structural trace feedback blocks."""
        if not self._socket:
            raise RuntimeError("Cannot await responses on an open network handle link.")
        
        raw_response = self._socket.recv(4096)
        if not raw_response:
            raise ConnectionResetError("Server terminated transmission pipeline channel prematurely.")

        response_text = raw_response.decode('utf-8')
        lines = response_text.split("\r\n")
        
        if not lines or not lines[0]:
            print("Invalid, unparseable or completely empty payload header returned.")
            return
        
        # Isolate Status Line tokens: e.g., ['HTTP/1.1', '200', 'OK']
        status_parts = lines[0].split(maxsplit=2)
        if len(status_parts) < 2:
            print(f"Corrupted HTTP header signature returned: {lines[0]}")
            return

        status_code = status_parts[1]
        
        print(f"\n--- [Server Low-Level Raw Network Echo] ---")
        print(response_text.strip())
        print("------------------------------------------")

        # Evaluate response metrics defensively using pattern matching properties
        match status_code:
            case _ if status_code.startswith("20"):
                print(f"Transaction Success! Status Code Match: {status_code}")
            case "404":
                print(f"Routing Fault Error: Target resource not found (404)")
            case "405":
                print(f"Semantic Policy Error: Method Not Allowed (405)")
            case "400":
                print(f"Protocol Formatting Error: Bad Request Structure (400)")
            case _:
                print(f"Unmapped operational feedback marker received: {status_code}")

    def start_repl_loop(self) -> None:
        """Triggers the primary prompt console loop interaction framework environment."""
        while True:
            try:
                print("\n=== REST API Socket Engine Shell ===")
                print("1. GET    3. PUT     5. Exit Interface")
                print("2. POST   4. DELETE")
                print("------------------------------------")
                print("Selection (1-5): ", end="", flush=True)

                choice = sys.stdin.readline().strip()
                if choice in ("5", "exit", "quit"):
                    print("Exiting application control flow loop.")
                    break

                match choice:
                    case "1" | "4":
                        method = "GET" if choice == "1" else "DELETE"
                        print("Enter target path endpoint: ", end="", flush=True)
                        target_path = sys.stdin.readline().strip()
                        with self:
                            self.send_http_request(method, target_path)
                            self.receive_and_parse_response()

                    case "2" | "3":
                        method = "POST" if choice == "2" else "PUT"
                        print("Enter target path endpoint: ", end="", flush=True)
                        target_path = sys.stdin.readline().strip()
                        
                        # Decoupled target variable paths completely avoiding payload overwrite traps
                        print('Enter string body details: ', end="", flush=True)
                        payload_body = sys.stdin.readline().strip()
                        
                        with self: 
                            self.send_http_request(method, target_path, body=payload_body)
                            self.receive_and_parse_response()

                    case _:
                        print("Input Choice must match a listed selection (1-5).")

            except (KeyboardInterrupt, SystemExit):
                print("\nSession killed via hardware terminal close command.")
                break
            except Exception as loop_fault:
                self.logger.error(f"Execution handling cycle failed downstream: {loop_fault}")
                break
