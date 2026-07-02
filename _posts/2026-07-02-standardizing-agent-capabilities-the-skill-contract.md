---
layout: default
title: "Standardizing Agent Capabilities: Implementing the Skill Contract"
description: "Architecting a plug-and-play skill registry to decouple business logic from agent orchestration."
---

- Author: **Amin Boulouma**, *Software Engineer*
- **Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
- **Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# Standardizing Agent Capabilities: The Skill Contract

In the early days of building AI agents, we often hardcode tool execution logic directly into our orchestrators. As the number of agents grows, the `AgentRunner` becomes a bloated monolith, rife with `if/else` statements and fragile dependency injection. When an engineer needs to add a new capability—say, a complex database query or a new web-scraping routine—they end up refactoring the entire core.

**The pain point:** Tight coupling between the **Orchestrator** (the brain) and the **Skill** (the muscle).

### Why we choose the "Skill-First" Contract
By implementing a formal `Skill` interface, we enforce a strict **Contract-First** architecture. This ensures that the Agent runner only cares about the *interface*, not the *implementation details*. If the database engine changes, the skill logic updates, but the `AgentRunner` remains blissfully unaware.



## Implementation

### Simple Example: The Base Contract
This ensures every module implements the `execute` method, preventing runtime failures when the agent attempts to call an undefined tool.

```python
from abc import ABC, abstractmethod
from typing import Any, Dict

class Skill(ABC):
    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Standardized interface for all skills."""
        pass

```

### Complex Example: Production-Grade Skill with Telemetry

In a production system, we need more than just execution; we need **lifecycle management**, **telemetry**, and **error isolation**.

```python
import time
import functools
import logging

class ProductionSkill(Skill):
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)

    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        start_time = time.perf_counter()
        try:
            # Business Logic
            result = self.run_logic(params)
            
            # Telemetry Injection
            duration = time.perf_counter() - start_time
            self.logger.info(f"Skill {self.name} completed in {duration:.4f}s")
            
            return {"status": "success", "data": result}
        except Exception as e:
            self.logger.error(f"Skill {self.name} failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    @abstractmethod
    def run_logic(self, params: Dict[str, Any]) -> Any:
        pass

```

## Quick Reference: Why Standardize?

| Concept | Naive Approach | Enterprise Approach |
| --- | --- | --- |
| **Interface** | Ad-hoc function calls | `Skill` Abstract Base Class |
| **Validation** | In-function `if` checks | `@validate_input` decorators |
| **Telemetry** | Manual logging inside logic | Middleware wrapper/Decorator |
| **Coupling** | High (Orchestrator knows logic) | Low (Interface based) |

## Developer Checklist

* [ ] **Contract Compliance**: Does the new module inherit from the base `Skill` class?
* [ ] **Schema Definition**: Is the input parameter structure documented for LLM consumption?
* [ ] **Exception Safety**: Is the skill wrapped in a `try-except` block to prevent system-wide crashes?
* [ ] **Async Readiness**: Is the execution non-blocking for I/O bound tasks?

## Final Takeaways

The transition from "scripting agents" to "building AI systems" requires a shift toward **modularity**. By treating every capability as a pluggable, isolated unit, you reduce technical debt and allow your agents to scale horizontally. **Standardization is not bureaucracy; it is the prerequisite for velocity.**
