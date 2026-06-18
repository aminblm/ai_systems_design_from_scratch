import ai_systems_design.utils as utils


class Container_Manager_CLI_client:
    def __init__(self, container_manager_server_host, container_manager_server_port):
        self.container_manager_server_host = container_manager_server_host
        self.container_manager_server_port = container_manager_server_port

    def start_CLI_interface(self):
        client_socket = utils.connect_to_socket_server(self.container_manager_server_host, self.container_manager_server_port, 'Container Manager')

        while True:
            try:
                command = input("Enter command (run, stop or list), exit to quit interface: ")

                if command == "quit": client_socket.sendall("exit".encode('utf-8')); break

                if command == 'run':
                    container_name = input("Enter container name: ").strip()
                    if len(container_name) < 1: print("Container name required"); continue
                    client_socket.sendall(f'run {container_name}'.encode('utf-8'))
                elif command == 'stop':
                    container_name = input("Enter container name: ").strip()
                    if len(container_name) < 1: print("Container name required"); continue
                    client_socket.sendall(f'stop {container_name}'.encode('utf-8'))
                elif command == 'list': client_socket.sendall(f'list'.encode('utf-8'))

            except Exception as e:
                print(f'Error: {e}')
                client_socket.sendall("Connection closed.".encode('utf-8'))
                break


if __name__ == '__main__':
    client = Container_Manager_CLI_client('127.0.0.1', 8080)
    client.start_CLI_interface()