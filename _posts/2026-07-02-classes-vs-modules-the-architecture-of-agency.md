---
layout: default
title: "Classes vs. Modules: Architecting for Dynamic Agent Discovery"
description: "Why the @tool decorator is the missing link between static Python code and truly autonomous AI agency."
---

- Author: **Amin Boulouma**, *Software Engineer*
- **Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
- **Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# Classes vs. Modules: The Architecture of Agency

In Python, the line between a **Class** and a **Module** is often blurred, leading many engineers to default to classes for everything. However, in the realm of AI agents, choosing the wrong abstraction creates a massive hurdle for auto-discovery. If your tools are hidden behind complex instantiation logic, your orchestrator will never find them.

**The pain point:** Hardcoding tool registration forces you to manually update a registry every time you add a capability. This creates a bottleneck that prevents true **Dynamic Agency**.

### The Fundamental Distinction
* **Modules (The Namespace):** Best for grouping stateless utility functions or constants. Use these when you don't need to maintain state across multiple calls.
* **Classes (The Blueprint):** Best for stateful instruments. If a tool needs to maintain a connection, a cache, or configuration, it *must* be a class.



## Implementation: The @tool Decorator

To transition from "passive code" to "discoverable instruments," we use a metadata-driven approach. By using a `@tool` decorator, we register the function or class in a central registry automatically during the application boot phase.

### Simple Example: Functional Module Tool
Use this for stateless operations where the logic is simple and requires no persistent state.

```python
# registry.py
TOOL_REGISTRY = {}

def tool(func):
    TOOL_REGISTRY[func.__name__] = func
    return func

# calculator.py
@tool
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

```

### Complex Example: Stateful Class Tool

For production systems, your tools often interact with external APIs or databases. You need a Class-based approach that maintains state (like an authenticated session) but remains discoverable.

```python
class ToolRegistry:
    _tools = {}

    @classmethod
    def register(cls, func_or_class):
        cls._tools[func_or_class.__name__] = func_or_class
        return func_or_class

class DatabaseQueryTool:
    def __init__(self, connection_string: str):
        self.db = self._connect(connection_string)

    def execute(self, query: str):
        return self.db.execute(query)

# Registration
ToolRegistry.register(DatabaseQueryTool)

```

## Why We Choose Decorators over Manual Registration

We chose **Decorator-based auto-discovery** over manual registration to eliminate the "Configuration Drift" where developers forget to add new tools to the main runner. By having the tool "advertise" itself during the module import, you ensure 100% visibility of all available capabilities.

## Quick Reference: When to use which?

| Strategy | Use Case | Why? |
| --- | --- | --- |
| **Module-level Function** | Atomic, stateless utilities | Lowest overhead, easy to unit test. |
| **Class-based Tool** | Stateful, resource-heavy | Encapsulates connection lifecycle & state. |
| **Decorator Pattern** | Global Discovery | Decouples registration from orchestration. |

## Developer Checklist

* [ ] **Stateless vs. Stateful**: Does my tool require persistent state? If yes, use a Class.
* [ ] **Auto-Registration**: Is the `@tool` decorator applied at the top level of the module?
* [ ] **Docstring Metadata**: Does the function/class have a clear docstring for LLM consumption?
* [ ] **Isolation**: Is the tool logic separated from the registration logic?

## Final Takeaways

Standardizing your tools via decorators turns your codebase into a "capabilities library." By separating the **Discovery** (via decorators) from the **Execution** (via the `AgentRunner`), you can scale your system to hundreds of tools without increasing the complexity of your core orchestrator.
