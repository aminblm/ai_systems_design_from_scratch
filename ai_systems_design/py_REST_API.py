import ai_systems_design.utils as utils


class REST_API:
    def __init__(self, host, port):
        self.host = host
        self.port = port 

    def start_server(self):
        server_socket = utils.create_socket_server(self.host, self.port, 'REST API')

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")

            # Read HTTP request
            request = client_socket.recv(4096).decode('utf-8')
            print(f'Received request: {request}')

            # Parse request
            method, path = self._parse_request(request)
            print(method, path)

            # Handle request
            response = self._handle_request(method, path)

            # Send response
            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()


    def _parse_request(self, request):
        return request.splitlines()[0].split()[0], request.splitlines()[0].split()[1]
    
    def _handle_request(self, method, path):
        if method == 'GET':
            if path == '/':
                response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\nHello, World!"
            elif path == '/hello': 
                response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\nHello from the server!"
            else:
                response = "HTTP/1.1 404 Not Found\nContent-Type: text/plain\n\nFile not found!"
        elif method == 'POST':
            # Handles form data or JSON
            print("Received POST data")
            response = "HTTP/1.1 201 Created\nContent-Type: application/json\n\n{'message': 'Data Received'}"
        elif method == 'PUT':
            # Handles update
            print("Data received!")
            response = "HTTP/1.1 200 OK\nContent-Type: application/json\n\nData Updated!"
        elif method == 'DELETE':
            response = "HTTP/1.1 200 OK\nContent-Type: text/plain\n\nData Deleted!"
        else:
            response = "HTTP/1.1 405 Method not allowed\nContent-Type: text/plain\n\nMethod not allowed!"
        return response
    
if __name__ == "__main__":
    app = REST_API('127.0.0.1', 8080)
    app.start_server()