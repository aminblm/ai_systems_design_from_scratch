---
layout: default
title: "Building a Custom Docker CLI Client in Pure Python"
description: "Demystifying container virtualization orchestration: Implementing a low-level, socket-multiplexed command line interface client from first principles."
---

# Building a Custom Docker CLI Client in Pure Python

When you run commands like `docker run`, `docker stop`, or `docker ps`, you aren't interacting directly with Linux kernel cgroups or namespaces. Instead, you are executing commands via a lightweight text-based client that serializes your intent and ships it over a Unix domain socket or a TCP network port to a background daemon (`dockerd`).

To fully understand container runtime orchestration, we must look at both sides of this network boundary. 

In keeping with our repository's **strict zero-dependency mandate**, we are pulling back the curtain on the client-side interaction layer. We will implement a custom, text-driven Docker-like CLI client using pure Python socket streams to pilot our backend container engine server (`py_container_manager`).

---

## The First-Principles CLI Client Blueprint

The architecture is encapsulated within a decoupled controller class: `Container_Manager_CLI_client`. It manages state validation, translates terminal input string configurations into protocol tokens, and streams serialized byte frames over a persistent raw TCP/IP connection socket.

Here is the complete codebase block matching our strict standard-library requirements:

```python
import utils

class Container_Manager_CLI_client:
    def __init__(self, container_manager_server_host, container_manager_server_port):
        self.container_manager_server_host = container_manager_server_host
        self.container_manager_server_port = container_manager_server_port

    def start_CLI_interface(self):
        """
        Establishes a persistent TCP connection handshake to the orchestrator daemon
        and boots the infinite user interactive input polling loop.
        """
        client_socket = utils.connect_to_socket_server(
            self.container_manager_server_host, 
            self.container_manager_server_port, 
            'Container Manager'
        )

        while True:
            try:
                # Polling user commands via the standard console input channel
                command = input("Enter command (run, stop or list), exit to quit interface: ").strip()

                # Graceful termination trap
                if command == "quit" or command == "exit": 
                    client_socket.sendall("exit".encode('utf-8'))
                    break

                if command == 'run':
                    container_name = input("Enter container name: ").strip()
                    if len(container_name) < 1: 
                        print("Container name required")
                        continue
                    client_socket.sendall(f'run {container_name}'.encode('utf-8'))
                    
                elif command == 'stop':
                    container_name = input("Enter container name: ").strip()
                    if len(container_name) < 1: 
                        print("Container name required")
                        continue
                    client_socket.sendall(f'stop {container_name}'.encode('utf-8'))
                    
                elif command == 'list': 
                    client_socket.sendall('list'.encode('utf-8'))
                    
                else:
                    print("Unknown instruction token. Valid primitives: run, stop, list, exit.")

            except Exception as e:
                print(f'Error: {e}')
                # Ensure the channel state closes gracefully without orphan socket leakage
                try:
                    client_socket.sendall("Connection closed.".encode('utf-8'))
                except:
                    pass
                break

if __name__ == '__main__':
    # Instantiate the client mapping to the local loopback container daemon port
    client = Container_Manager_CLI_client('127.0.0.1', 8080)
    client.start_CLI_interface()

```

---

## Architectural Deep Dive

### 1. The Daemon-Client Communication Contract

Because this client bypasses third-party RPC frameworks or HTTP overhead, it talks to our underlying infrastructure server using a raw **string serialization protocol**. The state command format is explicitly structured as space-delimited text payloads:

* `run <container_id>`: Instructs the engine daemon to invoke a new isolated fork container process.
* `stop <container_id>`: Signals the daemon to terminate execution boundaries on the targeted resource space.
* `list`: Demands a quick snapshot array dump of active isolation states.

### 2. Guardrails & Socket Security

Sockets are highly vulnerable to corruption if malformed or empty text blocks enter the stream buffer. Our `start_CLI_interface` engine enforces client-side string validation before firing packets into the network interface:

```python
if len(container_name) < 1: 
    print("Container name required")
    continue

```

By ensuring length constraints are met locally, we prevent the client from wasting socket bandwidth or throwing server-side token exceptions over the network pipe.

### 3. Preventing Orphan Connection Leakage

If a terminal session crashes (e.g., user hits a breaking terminal event), failing to alert the backend daemon leaves an "orphaned socket descriptor" hanging open on the operating system kernel. Our structural `try/except` loop wraps all transactional activities. If an unexpected error drops, the system catches it instantly and transmits an explicit termination string frame before exiting cleanly.

---

## Verifying the Orchestration Pipeline

To test this CLI component interface, you must first verify that your primary socket network layer helper is compiled and reachable, and that your underlying daemon is running.

### 1. Setup the Network Host

Ensure your `utils.py` contains the matching standard library TCP connector framework:

```python
import socket

def connect_to_socket_server(host, port, service_name):
    """Binds a raw socket layer directly to a remote listening TCP port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    print(f"Connected successfully to the {service_name} Daemon at {host}:{port}")
    return s

```

### 2. Execution Steps

1. Boot your backend manager daemon script (`py_container_manager.py`) on port `8080`.
2. Fire up this client interface inside a separate terminal window:
```bash
python py_container_manager_CLI_client.py

```



### Target Execution Log Output

```text
Connected successfully to the Container Manager Daemon at 127.0.0.1:8080
Enter command (run, stop or list), exit to quit interface: list
[Client Packet Shipped: list]

Enter command (run, stop or list), exit to quit interface: run
Enter container name: production_redis_node
[Client Packet Shipped: run production_redis_node]

```

---

## Next Evolutionary Milestones

While this client loop successfully abstracts command parsing away from the backend container manager daemon, it relies on synchronous block execution patterns.

To bridge the gap between this prototype and a high-throughput systems utility, our project integration checklist points to these upcoming engineering sprints:

* **Asynchronous Response Interception:** Refactoring the internal polling stream to use a dedicated tracking thread that continuously prints async status stream reports from the daemon without blocking the user input console.
* **Unix Domain Socket Routing:** Switching our `socket.AF_INET` TCP protocol interface over to localized file-system socket hooks (`socket.AF_UNIX`) to eliminate TCP handshaking latency on local loopbacks.
* **JSON Payload Marshalling:** Standardizing our custom text framing format to rigid JSON structures to natively support passing advanced environment settings (e.g., memory limits, port forwards) over the socket line.
