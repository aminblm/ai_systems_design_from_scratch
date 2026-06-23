---
layout: default
title: "Building a Pure HTTP Client over Raw Sockets"
description: "Demystifying application-layer transport protocols: Implementing a declarative REST API client using pure Python socket descriptors."
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

# Building a Pure HTTP Client over Raw Sockets

<div class="author-card">
    <p><strong>Amin Boulouma</strong> — <i>Software Engineer</i></p>
</div>

When we utilize abstractions like `requests.get()` in Python or `fetch()` in JavaScript, we are interacting with high-level clients wrapped around an application-layer network protocol: **Hypertext Transfer Protocol (HTTP)**. Beneath these convenient libraries, an HTTP request is nothing more than a structured ASCII text payload transmitted across a raw, transport-layer TCP socket stream.

To build a rugged understanding of systems engineering, we must strip away modern dependency wrappers and look directly at the underlying protocol specifications.

Adhering to our repository’s **strict zero-dependency mandate**, we will engineer an interactive REST API verification client entirely from first principles using pure Python socket management.

---

## The Socket-Driven HTTP Client Architecture

Our implementation uses an explicit class structure (`REST_API_CLI_Client`). This service connects to an underlying server socket channel, handles dynamic application state logic in an interactive menu loop, and manually constructs, serializes, and parses plain-text HTTP framing buffers.

Here is the complete codebase block matching our framework specifications:

```python
import socket
import utils

class REST_API_CLI_Client:
    def __init__(self, server_ip='127.0.0.1', server_port=8080):
        self.server_ip = server_ip
        self.server_port = server_port 

    def start_client(self):
        """Establishes a persistent transport connection to the target REST backend server."""
        client_socket = utils.connect_to_socket_server(self.server_ip, self.server_port, 'REST API')
        
        # Launch the core Command Line Interface polling state machine
        self._CLI_interface(client_socket)

    def _CLI_interface(self, client_socket):
        """Drives the user input selection loop and routes terminal parameters."""
        while True:
            try:
                print("\n=== REST API Tester ===")
                print("Available commands:")
                print("1. GET /path")
                print("2. POST /path [body]")
                print("3. PUT /path [body]")
                print("4. DELETE /path")
                print("5. Exit")
            
                choice_raw = input("Enter your choice (1-5): ").strip()
                if not choice_raw:
                    continue
                    
                if choice_raw == '5':
                    print("Severing transport path. Goodbye.")
                    client_socket.close()
                    break
                
                choice = int(choice_raw)
                
                if choice == 1:
                    path = input("Enter path e.g. /hello: ").strip()
                    self._send_request(client_socket, 'GET', path)
                elif choice == 2:
                    path = input("Enter path e.g. /data: ").strip()
                    body = input('Enter body e.g. {"key":"value"}: ').strip()
                    self._send_request(client_socket, 'POST', path, body)
                elif choice == 3:
                    path = input("Enter path e.g. /data: ").strip()
                    body = input('Enter body e.g. {"key":"value"}: ').strip()
                    self._send_request(client_socket, 'PUT', path, body)
                elif choice == 4:
                    path = input("Enter path e.g. /data: ").strip()
                    self._send_request(client_socket, 'DELETE', path)
                else:
                    print("Invalid command. Try again.")
                    
            except ValueError:
                print("Error: Input token must be an integer sequence.")
            except (KeyboardInterrupt, EOFError):
                print("\n\nProcess interrupted. Safe client shutdown executed.")
                client_socket.close()
                break

    def _send_request(self, client_socket, method, path, body=None):
        """Constructs compliance-valid HTTP raw network frames and flushes the socket wire."""
        # 1. Structural Application Layer Frame Assembly (\r\n transitions are mandatory)
        request_line = f"{method} {path} HTTP/1.1\r\n"
        
        if body:
            # Append required headers for structured payload ingestion
            request_line += "Content-Type: application/x-www-form-urlencoded\r\n"
            request_line += f"Content-Length: {len(body)}\r\n\r\n{body}\r\n"
        else:
            # Terminate HTTP headers block with an empty carriage-return newline pair
            request_line += "\r\n"

        # 2. Serialize ASCII text blocks to raw bytes and flush completely down the stream
        client_socket.sendall(request_line.encode('utf-8'))

        # 3. Read raw stream response chunks back from the kernel networking interface buffer
        response = client_socket.recv(4096).decode('utf-8')
        print("\n--- RAW HTTP RESPONSE FROM DAEMON ---")
        print(response)
        print("--------------------------------------")

        # 4. Route payload frame to the translation parser
        self._parse_response(response)

    def _parse_response(self, response):
        """Deconstructs wire responses into explicit application status elements."""
        if not response.strip():
            print("Received empty payload block.")
            return

        lines = response.splitlines()
        
        # Isolate Status Code (e.g. "HTTP/1.1 200 OK" -> "200")
        status_code = lines[0].split()[1]
        
        # Isolate dynamic headers from body segments
        headers = lines[1:-2]
        body = lines[-1] if len(lines) > 2 else None 
        
        print(f"Status: {status_code}")
        if body and body.strip(): 
            print("Body:", body)
        else: 
            print("Headers:", headers)

        # Evaluate response boundaries against REST status mappings
        if status_code.startswith("20"): 
            print("Success!")
        elif status_code == "404": 
            print("Error: Not found!")
        elif status_code == "405": 
            print("Error: Method not allowed!")
        else: 
            print("Unknown status envelope encountered.")


if __name__ == "__main__":
    client = REST_API_CLI_Client('127.0.0.1', 8080)
    client.start_client()

```

---

## Architectural Mechanisms Breakdown

### 1. The HTTP Plain-Text Specification (RFC 7230)

The absolute core of our script is the clean construction of the `request_line` block:

```python
request_line = f"{method} {path} HTTP/1.1\r\n"

```

HTTP/1.1 is an open text-based wire standard. It explicitly dictates that every parameter line boundary must terminate with a strict Carriage Return + Line Feed sequence (`\r\n`). When passing complex request payloads like `POST` or `PUT`, adding headers like `Content-Length` is mandatory. Without this exact header value, an downstream compliance-valid HTTP backend will choke, fail to identify where your request payload ends, and leave your connection hanging indefinitely.

### 2. Client-Side Parsing and Delimiter Splitting

Just as the client manually builds requests, it must also manually split incoming web responses. When parsing response packets, our method leverages native string operations like `.splitlines()`. This action breaks down the complete response block, letting the client easily step through and extract crucial header markers:

```python
status_code = lines[0].split()[1]

```

By segmenting arrays this way, our logic isolates status tokens out of the index frame effortlessly—mirroring how heavy proxy tools analyze web traffic under the hood.

### 3. State Rectification Guardrails

The original implementation had an overlapping input assignment typo under `choice == 2` and `choice == 3` that overwrote the `path` variable string with user request bodies. We re-engineered these flows into distinct variable buffers:

```python
path = input("Enter path e.g. /data: ").strip()
body = input('Enter body e.g. {"key":"value"}: ').strip()

```

This structural correction ensures that when `_send_request` fires, both structural arguments retain pristine values, avoiding critical route corruption issues.

---

## Verifying the REST Client Session

To verify your custom HTTP framework engine, launch it directly against a local server destination listener (or an equivalent script like `py_http_server.py`) run on port `8080`.

```bash
python py_http_client.py

```

### Target Execution Session Simulation Log

```text
=== REST API Tester ===
Available commands:
1. GET /path
2. POST /path [body]
3. PUT /path [body]
4. DELETE /path
5. Exit
Enter your choice (1-5): 1
Enter path e.g. /hello: /hello

--- RAW HTTP RESPONSE FROM DAEMON ---
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 12

Hello World!
--------------------------------------
Status: 200
Body: Hello World!
Success!

```

---

## Next Evolutionary Milestones

While this script successfully abstracts HTTP command compilation and response parsing loops, it functions as a simple prototype relying on clean loopback assumptions.

To upgrade this framework tool into a production-grade systems utility, our engineering roadmap features these milestones:

* **Chunked Transfer Stream Processing:** Refactoring `client_socket.recv(4096)` into a dynamic `while` chunk streaming consumer loop capable of re-assembling high-density binary files or web pages across network buffers.
* **Automatic JSON Content Type Marshalling:** Upgrading the body builder to automatically wrap inputs using Python's `json.dumps()`, and injecting modern `Content-Type: application/json` headers natively.
* **TLS Layer Handshaking Wrappers:** Wrapping our raw transport layer using Python's built-in `ssl.wrap_socket()` helper module to safely establish secure HTTPS operations over external networks.

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>