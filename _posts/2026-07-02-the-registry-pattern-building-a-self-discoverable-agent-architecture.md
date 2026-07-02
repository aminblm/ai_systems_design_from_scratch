---
layout: default
title: "The Registry Pattern: Building a Self-Discoverable Agent Architecture"
description: "How to use Python’s inspection capabilities to create a dynamic, self-documenting tool registry for AI agents."
---

- Author: **Amin Boulouma**, *Software Engineer*
- **Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
- **Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# The Registry Pattern: Building a Self-Discoverable Agent Architecture

In a mature AI system, the **Agent** should not be responsible for knowing which tools exist. Instead, the system architecture should facilitate a "Discovery Phase." Hardcoding tool lists into an Agent’s prompt or configuration file is the primary reason for brittle, non-scalable AI applications. When you add a new capability, you shouldn't have to update the Agent's brain.

**The pain point:** Tight coupling between tool availability and orchestration logic, leading to "knowledge rot" where the Agent is unaware of new system capabilities.

### The Power of Introspection
By leveraging Python's `inspect` module at load time, we can create a system where the code describes itself. This allows for a **declarative architecture** where you only define *what* a tool does, and the system handles *how* to expose it to the agent.



## Implementation

### Simple Example: The Basic Registry
This snippet demonstrates how a decorator can intercept a function and register its signature into a central, searchable store.

```python
class Registry:
    _tools = {}

    @classmethod
    def register(cls, func):
        cls._tools[func.__name__] = func
        return func

# Exposed tool
@Registry.register
def get_status():
    """Returns the current system health."""
    return "OK"

```

### Complex Example: Enterprise-Grade Introspection

In a production system, we must handle **type validation** and **metadata extraction** to prevent the Agent from passing malformed data to critical infrastructure.

```python
import inspect
import functools

class ToolRegistry:
    _registry = {}

    @classmethod
    def register(cls, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Pre-flight validation logic can be injected here
            return func(*args, **kwargs)
        
        # Capture metadata for Agent "Self-Awareness"
        cls._registry[func.__name__] = {
            "func": wrapper,
            "doc": inspect.getdoc(func),
            "params": {
                name: param.annotation.__name__ if hasattr(param.annotation, '__name__') else str(param.annotation)
                for name, param in inspect.signature(func).parameters.items()
            }
        }
        return wrapper

```

## Why we chose Registry Pattern over Config Files

Config files (JSON/YAML) are **static**. They get out of sync with your code, they are prone to human error, and they lack the ability to express complex logic. The **Registry Pattern** is dynamic; it resides inside the runtime, ensuring that your tools and your agent's knowledge are always in perfect alignment at the moment of startup.

## Quick Reference: Registry Scaling

| Feature | Manual Registration | Registry Pattern |
| --- | --- | --- |
| **New Tool Overhead** | High (Update config + code) | Low (Only add decorator) |
| **Doc Accuracy** | Manual / Out of sync | Automatic / Always current |
| **Type Safety** | Fragile | Enforced via Signature Inspection |
| **Agent Discovery** | Fixed | Dynamic (Query-based) |

## Developer Checklist

* [ ] **Type Annotations**: Are all tool parameters explicitly typed to allow for registry validation?
* [ ] **Docstring Clarity**: Does each tool's docstring explain *when* it should be used, not just *what* it does?
* [ ] **Registration Hooks**: Does the system log an alert if a duplicate tool name is registered?
* [ ] **Namespace Separation**: Are tools organized into logical modules?

## Final Takeaways

The Registry Pattern is the foundation of **Agent Autonomy**. By offloading the burden of tool management to an automated registry, you transform your system from a collection of scripts into a **Self-Discoverable Platform**.
