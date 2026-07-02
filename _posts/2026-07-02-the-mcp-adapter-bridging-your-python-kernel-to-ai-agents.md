---
layout: default
title: "The MCP Adapter: Bridging Your Python Kernel to AI Agents"
description: "How to implement an MCP Adapter to make your existing internal tools natively discoverable and callable by AI assistants."
---

- Author: **Amin Boulouma**, *Software Engineer*
- **Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
- **Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# The MCP Adapter: Bridging Your Python Kernel to AI Agents

You have built a robust suite of internal tools, registered via decorators, and organized in a registry. Yet, your AI agents still struggle to use them effectively because they lack a standardized communication protocol. When an AI assistant (like Claude) needs to interact with your system, it expects an **MCP (Model Context Protocol)** server. If your tools aren't "MCP-compliant," you end up writing custom, brittle glue-code for every new AI interface you support.

### Glossary for the Young Engineer
* **MCP (Model Context Protocol):** A standard way for AI to "plug in" to your computer programs, like plugging a lamp into a wall socket.
* **Adapter:** A piece of code that acts like a translator. It takes one language (your internal tool format) and translates it into another (MCP format).
* **Payload:** The actual message being sent. Think of it like the letter inside an envelope.
* **SSE (Server-Sent Events):** A way for a computer to keep sending updates to an AI without the AI having to keep asking "are you done yet?"

## The Problem Space: The "Glue Code" Trap
Without a standard interface, engineers often build ad-hoc REST endpoints for their tools. The AI has to "guess" how to call them, leading to hallucinations, incorrect parameter passing, and frequent integration breakage. 

**Why we choose an Adapter Pattern over rewriting APIs:** Rewriting your entire backend to match a new protocol is a waste of engineering time. An **Adapter** sits between your core logic and the outside world, mapping requests without changing the business logic itself.



## Implementation

### Simple Example: The Basic Adapter Logic
This shows how the adapter decides whether to list what it can do or actually perform a task.

```python
class SimpleMCPAdapter:
    def __init__(self, registry):
        self.registry = registry

    def handle(self, request):
        if request['method'] == "tools/list":
            return self.registry.keys()
        if request['method'] == "tools/call":
            return self.registry[request['params']['name']]()

```

### Complex Example: Production-Grade MCP Adapter

A production adapter must handle **method dispatching**, **schema translation**, and **error normalization** to comply with the JSON-RPC 2.0 specification required by MCP.

```python
import json

class MCPAdapter:
    def __init__(self, registry):
        self.registry = registry

    def handle_request(self, payload: dict):
        method = payload.get("method")
        params = payload.get("params", {})

        try:
            if method == "tools/list":
                return {"result": self._list_tools()}
            
            if method == "tools/call":
                return {"result": self._execute_tool(params)}
                
            raise ValueError("Method not found")
        except Exception as e:
            # Map Python errors to standard JSON-RPC error codes
            return {"error": {"code": -32603, "message": str(e)}}

    def _list_tools(self):
        return [{"name": n, "description": m['doc']} for n, m in self.registry._registry.items()]

```

## Quick Reference: Why MCP?

| Feature | Custom REST API | MCP Protocol |
| --- | --- | --- |
| **Discovery** | Manual (OpenAPI/Swagger) | Automatic (`tools/list`) |
| **Interaction** | Unstructured | Standardized (`tools/call`) |
| **Context** | Limited to Request/Response | Rich (Resources/Prompts/Tools) |

## Developer Checklist

* [ ] **Protocol Compliance**: Is the `tools/call` method handling JSON-RPC 2.0 error codes?
* [ ] **Security**: Are you validating that the agent is authorized to call the requested tool?
* [ ] **Observability**: Does your adapter log the incoming RPC request before execution?
* [ ] **SSE Compatibility**: Is your server-side implementation capable of pushing updates via SSE?

## Final Takeaways

1. **Never write AI-specific API endpoints.** Write your business logic once, and let the **Adapter** bridge it to any protocol.
2. **Standardization is reach.** An MCP-compliant tool works with any MCP client instantly, giving your code a massive multiplier on its utility.
3. **Handle errors gracefully.** When an AI calls a tool, the error message *is* the feedback the AI uses to correct its behavior—don't swallow it.
