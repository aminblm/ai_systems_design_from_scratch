---
layout: default
title: "Enforcing System Integrity: Abstract Base Classes as Protocols"
description: "Learn how to use Python's Abstract Base Classes (ABC) to establish strict module contracts, ensuring architectural consistency and predictable system orchestration."
---

# Enforcing System Integrity: Abstract Base Classes as Protocols

In large-scale enterprise software, the greatest challenge is maintaining coherence as the system expands. When dozens of developers contribute to different modules—databases, caches, logging services, or UI components—"interface drift" often occurs. One module expects a `connect()` method, while another expects `initialize()`. 

To solve this, we define a **Unified Interface Protocol** using Python’s `abc.ABC`. This creates a formal contract: any class claiming to be a system module *must* implement the required methods, or the code will refuse to run.



## The Protocol Contract

By moving definitions to `kernel/interface.py`, we shift the burden of compliance from the developer's memory to the compiler. This ensures that the central orchestrator (the Kernel) can manage diverse services without knowing their internal logic.

### 1. Simple Example: The Lifecycle Protocol
This basic contract ensures that every system component has a standardized way to boot and shut down.

```python
from abc import ABC, abstractmethod

class Service(ABC):
    @abstractmethod
    def start(self): pass

    @abstractmethod
    def stop(self): pass

class DatabaseService(Service):
    def start(self): print("Database online.")
    def stop(self): print("Database offline.")

# This would fail at instantiation if start/stop were missing
# db = DatabaseService() 

```

### 2. Complex Example: Orchestration Interface

In a professional setting, we combine the protocol with type hinting to ensure that even complex status reports remain predictable across the system.

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class Orchestratable(ABC):
    @abstractmethod
    def get_health(self) -> Dict[str, Any]:
        """Must return a health schema for monitoring."""
        pass

class MessageQueue(Orchestratable):
    def get_health(self) -> Dict[str, Any]:
        return {"status": "ok", "queue_depth": 42}

class APIProxy(Orchestratable):
    def get_health(self) -> Dict[str, Any]:
        return {"status": "degraded", "latency_ms": 150}

# The Kernel can now uniformly query any service
def monitor_system(services: list[Orchestratable]):
    for s in services:
        print(f"Service status: {s.get_health()}")

```

## Why Protocols Drive Scalability

* **Fail-Fast Development:** Developers discover missing implementations at initialization, not during a production outage.
* **Orchestration Simplicity:** The Kernel does not need `if-else` blocks to handle different service types; it only needs to know they all satisfy the `Orchestratable` contract.
* **Self-Documenting Code:** The abstract class acts as the system's "source of truth," clearly defining expectations for new features.

Adopting this protocol-first approach transforms a collection of scripts into a unified, enterprise-grade architecture.

- **Author: Amin Boulouma**, *Software Engineer*
- **Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
