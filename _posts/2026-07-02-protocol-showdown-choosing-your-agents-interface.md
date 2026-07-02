---
layout: default
title: "Protocol Showdown: Choosing Between RPC, HTTP, and Sockets for AI Agents"
description: "How to map your infrastructure to JSON-RPC 2.0 to make your systems natively compatible with AI orchestrators."
---

- Author: **Amin Boulouma**, *Software Engineer*
- **Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
- **Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# Protocol Showdown: Choosing Your Agent's Interface

When you move from simple scripts to an **MCP-ready ecosystem**, the transport layer you choose determines whether your AI can "speak" to your tools or whether it remains trapped behind a wall of incompatible code. Many engineers struggle because they equate "API" with "REST," ignoring the fact that AI-driven orchestration often requires bidirectional, stateful interaction.

### Glossary for the Young Engineer
* **RPC (Remote Procedure Call):** A way for one computer to ask another computer to run a function, acting like it’s running right there on its own machine.
* **HTTP:** The "language" of the internet. It’s like sending a letter through the post office—you send a request, and wait for a reply.
* **Sockets:** A permanent "telephone line" between two computers. Instead of mailing letters, you can talk back and forth as much as you want without hanging up.
* **JSON-RPC:** A standardized way to send these "run function" requests using a format that computers easily understand.

## The Problem Space: REST vs. Agency
In a standard **REST** architecture, you define resources (e.g., `/users/1`). However, agents don't think in terms of resources; they think in terms of **capabilities** (e.g., `fetch_weather()`). When you use REST for agents, you often end up creating "fake" endpoints that act like function calls, which is messy and non-standard.



**Why we choose JSON-RPC 2.0:** It is the "lingua franca" of the Model Context Protocol (MCP). It defines exactly how to list capabilities (`tools/list`) and how to invoke them (`tools/call`), providing a formal contract that an LLM can parse programmatically.

## Implementation

### Simple Example: The Basic HTTP REST Endpoint
This is the standard approach, but it lacks the formal structure required for automated agent discovery.

```python
# REST approach: Hard to document for AI agents
def get_user(user_id):
    return {"id": user_id, "name": "Amin"}

```

### Complex Example: JSON-RPC 2.0 Implementation

By adopting this structure, your service becomes natively discoverable by MCP-enabled clients.

```python
import json

class RPCServer:
    def __init__(self):
        self.methods = {}

    def register(self, name, func):
        self.methods[name] = func

    def handle_request(self, json_payload):
        req = json.loads(json_payload)
        method_name = req.get("method")
        params = req.get("params", {})
        
        if method_name in self.methods:
            result = self.methods[method_name](**params)
            return json.dumps({"jsonrpc": "2.0", "result": result, "id": req.get("id")})
        return json.dumps({"jsonrpc": "2.0", "error": "Method not found", "id": req.get("id")})

```

## Quick Reference: When to use which?

| Protocol | Use Case | Why? |
| --- | --- | --- |
| **HTTP/REST** | Public Web APIs | Familiar, caches well, universal support. |
| **JSON-RPC** | Agentic Tooling | Formalized "Tool Call" contract. |
| **Raw Sockets** | High-Frequency Trading | Minimal overhead, bidirectional speed. |

## Developer Checklist

* [ ] **Discovery**: Does your service implement `tools/list` to tell the agent what it can do?
* [ ] **Contract**: Is your JSON structure strictly compliant with the JSON-RPC 2.0 spec?
* [ ] **State**: Are you using WebSockets/Persistent Sockets if your agent needs to stream updates?
* [ ] **Error Handling**: Do you return standard error codes when a tool invocation fails?

## Final Takeaways

1. **REST is for documents; RPC is for actions.** If your AI needs to do things rather than just read things, move to RPC.
2. **Standardization is velocity.** By adopting JSON-RPC, you avoid building custom adapters for every new AI platform that comes along.
3. **Decouple the transport.** Your business logic should not care if it's accessed via HTTP or Sockets—keep that concern inside your `RPCServer` class.
