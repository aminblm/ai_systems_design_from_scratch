import utils


class ContainerManager:
    def __init__(self, host='127.0.0.1', listen_port=8080):
        self.containers = {}
        self.server_socket = None
        self.listen_port = listen_port
        self.host = host

    def start_server(self):
        """Start server listening on specified port."""
        self.server_socket = utils.create_socket_server(self.host, self.listen_port, 'Container Manager')

        while True:
            self.client_socket, self.client_address = self.server_socket.accept()
            print(f'Connection from {self.client_address}')
            self._handle_client()

    def _handle_client(self):
        """Handles a client connection and process commands."""
        while True:
            data = self.client_socket.recv(1024).decode('utf-8')
            if not data: break
            print(f'Received data: {data}')
            if not data.strip(): continue

            # Parse command
            parts = data.strip().split()
            if not parts: continue 

            command = parts[0]
            if command == 'run': 
                if len(parts) < 2: self.client_socket.sendall("Usage: run <container_name>".encode('utf-8')); continue
                self._run(parts)
            elif command == 'stop': 
                if len(parts) < 2: self.client_socket.sendall("Usage: stop <container_name>".encode('utf-8')); continue
                self._stop(parts)
            elif command == 'list': self._list()
            else: self.client_socket.sendall(f"Unknown command {command}".encode('utf-8'))

        self.client_socket.close()


    def _run(self, parts):
        container_name = parts[1]
        self.containers[container_name] = {
            'status': 'created',
            'file': f'/tmp/{container_name}.txt'
        }
        # TODO: Fix socket.sendall(...) so it sends the message to all
        # print(f"Container '{container_name} created at '{self.containers[container_name]['file']}'".encode('utf-8'))
        self.client_socket.sendall(f"Container '{container_name} created at '{self.containers[container_name]['file']}'".encode('utf-8'))

    def _stop(self, parts):
        container_name = parts[1]
        if container_name in self.containers:
            self.containers[container_name]['status'] = 'stopped'
            self.client_socket.sendall(f"Container '{container_name} stopped'".encode('utf-8'))
        else:
            self.client_socket.sendall(f'Container not found'.encode('utf-8'))

    def _list(self):
        clients = []
        for name, info in self.containers.items(): clients.append(f'{name} - {info['status']}')
        self.client_socket.sendall(f"Available containers: {clients}".encode('utf-8'))

if __name__ == "__main__":
    manager = ContainerManager()
    manager.start_server()