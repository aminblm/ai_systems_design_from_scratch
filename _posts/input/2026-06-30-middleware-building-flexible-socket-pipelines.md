---
title: "Implementing Middleware: Building Flexible Socket Pipelines"
description: "How to use the Chain of Responsibility pattern to decouple cross-cutting concerns in your socket server."
layout: default
---

# Middleware: Building Flexible Socket Pipelines

Middleware transforms a static server into a dynamic pipeline. Instead of hardcoding logic like logging, authentication, or payload transformation directly into your `SocketServer`, you delegate these responsibilities to a **chain of modular functions**.

## The Concept: Chain of Responsibility

Middleware allows you to intercept a request, perform an action, and decide whether to pass it to the next link in the chain or terminate the request early. 



## Why Use Middleware?

* **Separation of Concerns:** Your core server logic focuses on *handling* the socket connection, while middlewares handle *peripheral* tasks like header parsing, request sanitization, or request logging.
* **Declarative Configuration:** You can "plug and play" features. Need to add authentication? Just call `server.add_middleware(authenticate_request)`.
* **DRY (Don't Repeat Yourself):** Logic that is common across different request types is written once as a middleware and reused across the entire application.

## The Pipeline Flow

In the implementation provided, the request follows a strictly linear path:

1.  **Ingress:** The raw payload arrives from the socket.
2.  **Transformation (Middleware Chain):** Each registered middleware function receives the `request_text` and performs a transformation.
3.  **Core Logic:** The fully transformed string reaches the handler.
4.  **Egress:** The resulting output is returned to the client.

```python
# The Transformation Loop
for middleware in self._middlewares:
    request_text = middleware(request_text)

```

## Best Practices for Middleware Design

1. **Idempotency:** Try to ensure your middleware functions are predictable. Given the same input, they should reliably produce the same transformation.
2. **Order Matters:** In a middleware chain, the order of application is critical. For example, you must "decode" a payload before you "validate" the text format.
3. **Lightweight Processing:** Middleware runs for *every* request. Keep the logic inside these functions performant to ensure low latency.

## Summary: When to apply Middleware?

* **Logging/Observability:** Record metrics or request logs for every incoming connection.
* **Security:** Implement IP filtering, rate limiting, or authentication checks.
* **Data Sanitization:** Automatically strip sensitive characters, decode encoding schemes, or enforce character limits.

By treating your `SocketServer` as a pipeline rather than a monolith, you future-proof your network code against changing requirements.
