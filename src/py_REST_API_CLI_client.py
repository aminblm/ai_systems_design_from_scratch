import socket

import utils


class REST_API_CLI_Client:
    def __init__(self, server_ip='127.0.0.1', server_port=8080):
        self.server_ip = server_ip
        self.server_port = server_port 

    def start_client(self):
        # Connect to the server
        client_socket = utils.connect_to_socket_server(self.server_ip, self.server_port, 'REST API')

        # CLI Loop
        self._CLI_interface(client_socket)

    def _CLI_interface(self, client_socket):
        while True:
            print("\n=== REST API Tester ===")
            print("Available commands:")
            print("1. GET /path")
            print("2. POST /path [body]")
            print("3. PUT /path [body]")
            print("4. DELETE /path")
            print("5. Exit")
        
            choice = int(input("Enter your choice (1-5): ").strip())
            if choice == '5':break
            
            # Parse command
            if choice == 1:
                path = input("Enter path e.g. /hello: ").strip()
                self._send_request(client_socket, 'GET', path)
            elif choice == 2:
                path = input("Enter path e.g. /data: ").strip()
                path = input('Enter body e.g. {"key":"value"}: ').strip()
                self._send_request(client_socket, 'POST', path)
            elif choice == 3:
                path = input("Enter path e.g. /data: ").strip()
                path = input('Enter body e.g. {"key":"value"}: ').strip()
                self._send_request(client_socket, 'PUT', path)
            elif choice == 4:
                path = input("Enter path e.g. /data: ").strip()
                self._send_request(client_socket, 'DELETE', path)
            else:
                print("Invalid command. Try again.")

    def _send_request(self, client_socket, method, path, body=None):
        # Build HTTP request
        request_line = f"{method} {path} HTTP/1.1\r\n"
        if body: request_line += f"Content-Type: application/x-www-form-urlencoded\r\n: {len(body)}\r\n\r\n{body}\r\n"
        else: request_line += "\r\n"

        # Send request
        client_socket.sendall(request_line.encode('utf-8'))

        # Receive response
        response = client_socket.recv(4096).decode('utf-8')
        print(response)

        # Parse response
        self._parse_response(response)

    def _parse_response(self, response):
        
        status_code = response.splitlines()[0].split()[1]
        headers = response.splitlines()[1:-2]
        body = response.splitlines()[-1] if len(response.splitlines()) > 2 else None 
        
        print(f"Status: {status_code}")
        if body: print("Body:", body)
        else: print("Headers:", headers)

        if status_code.startswith("20"): print("Success!")
        elif status_code("404"): print("Error: Not found!")
        elif status_code("405"): print("Error: Method not allowed!")
        else: print("Unknown error!")

if __name__ == "__main__":
    client = REST_API_CLI_Client('127.0.0.1', 8080)
    client.start_client()