# rest_api_server.py
import json
from typing import Callable, Dict, Tuple, List
from functools import wraps

from ai_system_design.kernel.socket_server import SocketServer
from ai_system_design.kernel.logger import logger


class RESTAPIServer(SocketServer):
    def __init__(self, host, port, context="REST API") -> None:
        super().__init__(host, port, context)
        # Explicit route mapping tree structure
        # Layout: self._routes[HTTP_METHOD][URL_PATH] = Handler_Callback
        self._routes: Dict[str, Dict[str, Callable[[str], Tuple[int, str, str]]]] = {
            "GET": {}, "POST": {}, "PUT": {}, "DELETE": {}
        }
        self._register_core_endpoints()

    def register_endpoint(self, method: str, path: str, status: int, content_type: str, content: str) -> None:
        self._routes[method][path] = lambda body: (status, content_type, content)

    def get_endpoints(self) -> Dict[str, Dict[str, Callable[[str], Tuple[int, str, str]]]]:
        return self._routes.copy()
    
    def get_endpoints_documentation(self) -> Dict[str, List[str]]:
        doc: Dict[str, List[str]] = {}
        for k, v in self._routes.items():
            doc[k] = list(v.keys())
        return doc

    def get(self, path: str, content: str) -> None:
        """Register a GET Endpoint."""
        self._routes["GET"][path] = lambda body: (200, "text/plain", content)

    def post(self, path: str, content: str) -> None:
        """Register a POST Endpoint."""
        self._routes["POST"][path] = lambda body: (200, "application/json", content)

    def put(self, path: str, content: str) -> None:
        """Register a PUT Endpoint."""
        self._routes["PUT"][path] = lambda body: (200, "application/json", content)

    def delete(self, path: str, content: str) -> None:
        """Register a DELETE Endpoint."""
        self._routes["DELETE"][path] = lambda body: (200, "text/plain", content)

    def _register_core_endpoints(self) -> None:
        """Decouples application routing configuration definitions away from raw transport IO."""
        self._routes["GET"]["/"] = lambda body: (200, "text/plain", "Welcome to the AI System Design from First Principle Repository")
        self._routes["GET"]["/get-endpoints-documentation"] = lambda body: (200, "application/json", json.dumps(self.get_endpoints_documentation()))

    def start_http_server(self):
        """Spins up the master bound socket loop, isolating active connections to worker threads."""
        self.start_server(self._process_http_transaction)

    def _process_http_transaction(self, request_text: str) -> bytes:
        """Parses raw text frames and constructs fully compliant HTTP/1.1 response bytes."""
        lines = request_text.split("\r\n")
        if not lines or not lines[0].strip():
            # DEFENSIVE: Prevent crash if request starts with an empty frame line
            return self._build_http_response(400, "text/plain", "Bad Request: Empty Request Payload Data.")

        # Parse Request Line tokens: e.g., ["GET", "/hello", "HTTP/1.1"]
        request_tokens = lines[0].split()
        if len(request_tokens) < 2:
            return self._build_http_response(400, "text/plain", "Bad Request: Invalid Method/Path format tokens.")

        method, path = request_tokens[0].upper(), request_tokens[1]

        # Separate request body content from headers block if present
        body_content = ""
        if "\r\n\r\n" in request_text:
            body_content = request_text.split("\r\n\r\n", 1)[1]

        # Route validation execution pattern matching
        if method not in self._routes:
            return self._build_http_response(405, "text/plain", "Method Not Allowed")

        method_routes = self._routes[method]
        if path not in method_routes:
            return self._build_http_response(404, "text/plain", "404 Not Found: Path pattern matches nothing.")
        
        # Invoke targeted handler callback routine safely
        try:
            status, content_type, payload = method_routes[path](body_content)
            return self._build_http_response(status, content_type, payload)
        except Exception as route_err:
            logger.error(f"Internal Route Exception evaluating path '{path}': {route_err}")
            return self._build_http_response(500, "text/plain", "Internal Server Error")

    def _build_http_response(self, status_code: int, content_type: str, body: str) -> bytes:
        """Assembles compliant HTTP/1.1 text frames utilizing precise CRLF formatting structures."""
        status_phrases = {
            200: "OK", 201: "Created", 400: "Bad Request", 
            404: "Not Found", 405: "Method Not Allowed", 500: "Internal Server Error"
        }
        phrase = status_phrases.get(status_code, "Unknown")
        body_bytes = body.encode('utf-8')

        # Enforced standard \r\n line delimiters across all header lines
        response_headers = [
            f"HTTP/1.1 {status_code} {phrase}",
            f"Content-Type: {content_type}",
            f"Content-Length: {len(body_bytes)}",
            "Connection: close",
            "",  # Empty element yields the mandatory trailing double delimiter spacing line block
            body
        ]
        return "\r\n".join(response_headers).encode('utf-8')
