---
layout: default
title: "Building a Custom Docker Daemon Engine From Scratch"
description: "Demystifying container orchestration backends: Implementing a stateful, stream-oriented orchestration server with custom command processing in pure Python."
---

<head>
  <meta charset="utf-8">
  <title>{{ page.title }} | {{ site.title }}</title>
  <meta name="description" content="{{ page.description | default: site.description }}">
  <link rel="canonical" href="{{ site.url }}{{ site.baseurl }}{{ page.url }}">
  
  <meta property="og:type" content="article">
  <meta property="og:title" content="{{ page.title }}">
  <meta property="og:description" content="{{ page.description | default: site.description }}">
  <meta property="og:url" content="{{ site.url }}{{ site.baseurl }}{{ page.url }}">
  <meta property="og:site_name" content="{{ site.title }}">
  
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{{ page.title }}">
  <meta name="twitter:description" content="{{ page.description | default: site.description }}">
</head>

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

<a href="https://www.producthunt.com/products/ai-systems-design-from-first-principles?embed=true&amp;utm_source=badge-featured&amp;utm_medium=badge&amp;utm_campaign=badge-ai-systems-design-from-first-principles" target="_blank" rel="noopener noreferrer"><img alt="AI Systems Design From First Principles - An implementation of AI Systems Design From First Principles | Product Hunt" width="250" height="54" src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1173628&amp;theme=dark&amp;t=1781635927239"></a>

<div style="text-align: center; margin: 2rem 0; padding-bottom: 1rem; border-bottom: 1px solid #e9ebec;">
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">🏠 Documentation Hub</a>
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/blog" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">📝 Engineering Blog</a>
  <a href="https://github.com/aminblm/ai_systems_design_from_scratch" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">💻 GitHub Repository</a>
</div>


# Building a Custom Docker Daemon Engine From Scratch

<div class="author-card">
    <p><strong>{{ site.author.name }}</strong> — <i>{{ site.author.bio }}</i></p>
</div>

When you execute a command through a client CLI tool, it communicates directly with a central structural service: the container runtime daemon. In a production environment, this is `dockerd`. The daemon acts as the stateful engine room of the platform—listening continuously for incoming socket connection packets, validating requests against an internal data schema, spinning up virtual sandboxes, and logging operational status matrices.

By analyzing the daemon as a clean communication layer, we peel back the abstraction of infrastructure automation. 

To satisfy our repository's **strict zero-dependency constraint**, we will build a stateful, socket-multiplexed container virtualization coordinator server completely from scratch, relying solely on the Python standard library runtime.

---

## The Container Daemon Architecture

Our engine implementation relies on the `ContainerManager` class. This component coordinates three major architectural states:
1. **Network Demultiplexing:** Binding network infrastructure to intercept raw bytes.
2. **Dynamic Request Parsing:** Tokenizing incoming stream frames into executable structural steps (`run`, `stop`, `list`).
3. **State Management:** Tracking logical cluster workloads within memory boundary dictionaries.

Here is the complete first-principles daemon implementation:

```python
import utils

class ContainerManager:
    def __init__(self, host='127.0.0.1', listen_port=8080):
        self.containers = {}
        self.server_socket = None
        self.listen_port = listen_port
        self.host = host

    def start_server(self):
        """Initializes the listener socket pool and triggers the main listener loop."""
        self.server_socket = utils.create_socket_server(self.host, self.listen_port, 'Container Manager')

        while True:
            # Block thread processing until a new client establishes a socket connection
            self.client_socket, self.client_address = self.server_socket.accept()
            print(f'Connection from {self.client_address}')
            self._handle_client()

    def _handle_client(self):
        """Processes incoming data frames from an active connection pipe sequentially."""
        while True:
            data = self.client_socket.recv(1024).decode('utf-8')
            if not data: 
                break
            print(f'Received data: {data}')
            if not data.strip(): 
                continue

            # Tokenize serialization string into instruction arrays
            parts = data.strip().split()
            if not parts: 
                continue 

            command = parts[0]
            if command == 'run': 
                if len(parts) < 2: 
                    self.client_socket.sendall("Usage: run <container_name>".encode('utf-8'))
                    continue
                self._run(parts)
            elif command == 'stop': 
                if len(parts) < 2: 
                    self.client_socket.sendall("Usage: stop <container_name>".encode('utf-8'))
                    continue
                self._stop(parts)
            elif command == 'list': 
                self._list()
            else:
                self.client_socket.sendall(f"Unknown command {command}".encode('utf-8'))

        self.client_socket.close()

    def _run(self, parts):
        """Allocates resources and assigns an initial active status structure."""
        container_name = parts[1]
        self.containers[container_name] = {
            'status': 'created',
            'file': f'/tmp/{container_name}.txt'
        }
        # Transmit direct network receipt confirmation string
        self.client_socket.sendall(f"Container '{container_name}' created at '{self.containers[container_name]['file']}'".encode('utf-8'))

    def _stop(self, parts):
        """Alters container state mappings to reflect runtime termination."""
        container_name = parts[1]
        if container_name in self.containers:
            self.containers[container_name]['status'] = 'stopped'
            self.client_socket.sendall(f"Container '{container_name}' stopped".encode('utf-8'))
        else:
            self.client_socket.sendall('Container not found'.encode('utf-8'))

    def _list(self):
        """Compiles a complete serialization snapshot of active data fields."""
        clients = []
        for name, info in self.containers.items(): 
            clients.append(f"{name} - {info['status']}")
        self.client_socket.sendall(f"Available containers: {clients}".encode('utf-8'))

if __name__ == "__main__":
    manager = ContainerManager()
    manager.start_server()

```

---

## Architectural Mechanisms Breakdown

### 1. In-Memory State Registration

Unlike stateless API microservices, our daemon acts as a single source of truth using a localized tracking matrix: `self.containers`. When a `_run` sequence gets processed, the engine mutates this dictionary state. This models exactly how full-scale runtimes store configuration blobs, isolated virtual locations, and system parameters during local execution.

### 2. Stream Buffer Splitting & Parsing

Data moving over raw network sockets arrives without structural spacing formatting. By extracting string tokens using whitespace parsing checks:

```python
parts = data.strip().split()
command = parts[0]

```

The server isolates the functional command token and cross-references it against our structural execution blocks. The remaining elements are mapped dynamically as configuration arguments to drive target behaviors.

### 3. Connection Lifecycles & Resource Cleansing

When the client disconnects or an empty data string block (`if not data: break`) hits the transport layer, the controller drops out of its command handler loop and drops down to clean up socket allocations. Explicitly closing `self.client_socket` is crucial for production reliability; without it, file handles remain locked, slowly degrading system resources.

---

## Integration and Network Testing

To launch the daemon locally, make sure your shared network helper components are initialized within your codebase structure.

### 1. Bootstrap the Shared Socket Utilities

Ensure `utils.py` contains the matching server initialization routine:

```python
import socket

def create_socket_server(host, port, service_name):
    """Initializes and returns a reusable standard TCP server socket."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    print(f"{service_name} Daemon actively listening on {host}:{port}")
    return s

```

### 2. Execution Testing Sequence

Run the daemon backend within your core terminal instance:

```bash
python py_container_manager.py

```

Now, fire commands using your previously engineered command line interface tool (`py_container_manager_CLI_client.py`) to see the system parse status updates synchronously:

```text
Container Manager Daemon actively listening on 127.0.0.1:8080
Connection from ('127.0.0.1', 54321)
Received data: run micro_service_node
Received data: list

```

---

## Infrastructure Scaling Roadmap

While this server engine handles basic state tracking and command interpretation, it is constrained by a synchronous connection blocker: it can only handle a single client payload loop at a time.

To transform this system into a high-throughput runtime simulator, our upcoming milestones target these upgrades:

* **Non-Blocking Selectors / Threading:** Refactoring `start_server` to dispatch client connections onto individual `threading.Thread` loops or a non-blocking `selectors` module array to support dozens of concurrent client CLI processes.
* **OS Namespace Process Spawning:** Upgrading the `_run` strategy to dynamically spawn physical, isolated OS subprocesses using Python's `subprocess.Popen`, allowing for authentic process life-cycle monitoring.
* **Persistent Local Storage:** Transitioning the in-memory dictionary to write state change files continuously to disk, protecting your cluster's metadata from resetting if the server drops.

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>