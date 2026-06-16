import socket
import json 

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8029))
    server_socket.listen(1)
    print('Git server listening on port 8029...')

    while True: 
        client_socket, addr = server_socket.accept()
        print(f'Connection from {addr}')

        data = client_socket.recv(1024).decode()
        print(f'Received {data}')

        if not data: 
            client_socket.sendall(json.dumps({"error": "No data received"}).encode())
            continue

        try:
            # Example: "git clone https://github.com/user/repo.git"
            # Server respond with a mock clone 
            response = json.dumps({
                "type": "git",
                "command": "clone",
                "args": ["https://github.com/user/repo.git"],
                "status": "success",
                "message": "Cloned repository successfully"
            }).encode()
            client_socket.sendall(response)
        except Exception as e:
            client_socket.sendall(json.dumps({"error": str(e)}).encode())

        client_socket.close()

if __name__ == '__main__':
    start_server()