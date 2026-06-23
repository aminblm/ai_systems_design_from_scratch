---
title: "Building CRLF-Compliant HTTP Requests"
description: "Learn why CRLF line endings are critical for HTTP protocol adherence and how to prevent common request-splitting vulnerabilities."
layout: default
---

# Building CRLF-Compliant HTTP Requests

In the world of network protocols, the difference between a functional request and a security vulnerability often comes down to a few invisible characters. HTTP mandates the use of **CRLF** (Carriage Return + Line Feed, `\r\n`) to delimit headers and separate the header section from the body.

## Why CRLF Matters

The HTTP/1.1 specification (RFC 7230) explicitly requires `\r\n` as the line terminator. Many developers make the mistake of using standard Unix-style line endings (`\n`) when crafting raw HTTP requests.



### The Danger of Ignoring CRLF
1.  **Protocol Rejection**: Many robust web servers (like Nginx or Apache) are strictly compliant. Using only `\n` may cause your request to be rejected with a `400 Bad Request`.
2.  **Request Splitting/Smuggling**: If you allow user-supplied data to be injected into headers without sanitizing `\r` and `\n` characters, an attacker can craft a malicious string that terminates your request early and injects a completely different request—this is the foundation of **HTTP Request Smuggling**.

---

## Crafting Compliant Requests

Always build your headers as a list and join them with the mandatory `\r\n` sequence. Never trust raw user input to be properly formatted.

### The Idiomatic Way
```python
def create_http_request(method, path, headers: dict, body: str = ""):
    # 1. Define the Request Line
    request_line = f"{method} {path} HTTP/1.1"
    
    # 2. Join headers with CRLF
    header_lines = [f"{k}: {v}" for k, v in headers.items()]
    header_section = "\r\n".join(header_lines)
    
    # 3. Assemble: Header + Double CRLF + Body
    # The double CRLF (\r\n\r\n) is the required delimiter 
    # between the headers and the body.
    full_request = f"{request_line}\r\n{header_section}\r\n\r\n{body}"
    
    return full_request.encode('utf-8')

```

---

## Security Checklist

* **Sanitize Inputs**: Before inserting any variable into a header, strip out all `\r` and `\n` characters.
* **Use Libraries**: Whenever possible, use high-level libraries like `requests` or `httpx` instead of raw sockets. These libraries handle CRLF compliance and header encoding automatically.
* **Validate Delimiters**: If you must build raw requests, ensure the `\r\n\r\n` sequence appears exactly once, separating your header block from your payload.

---

## Comparison of Delimiter Handling

| Delimiter | Protocol Standard | Risk Level | Use Case |
| --- | --- | --- | --- |
| `\r\n` (CRLF) | Required (HTTP/1.1) | Safe | Network Protocols |
| `\n` (LF) | Non-compliant | High (Rejection/Smuggling) | Internal system logs |
| `\r` (CR) | Non-compliant | High | Legacy systems (avoid) |

By adhering to the CRLF standard, you ensure your requests are portable across different servers and safe from injection attacks.

---
