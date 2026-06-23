---
title: "Modular Design: Achieving Cohesion in Python"
description: "Learn how to enhance code maintainability and testability by extracting input handling and network logic into cohesive sub-methods."
layout: default
---

# Cohesive Sub-methods: The Path to Clean Orchestration

A common architectural trap in Python development is the "God Method"—a single, monolithic function that handles user input, processes business logic, and manages network communication. This creates code that is nearly impossible to test and terrifying to modify.

The solution is **Functional Cohesion**. By separating distinct responsibilities into dedicated sub-methods, you turn an opaque "orchestrator" into a clean, readable, and highly testable workflow.

## The Problem: The "God Method"
When input logic and network logic live in the same block, you cannot test your network code without simulating user input, and you cannot test your input validation without triggering network calls.



---

## The Solution: Extraction and Delegation

To improve cohesion, extract specific tasks into their own methods. Your main orchestrator then becomes a simple "driver" that tells other parts of the system what to do.

### The Refactored Pattern
```python
class GitTaskOrchestrator:
    def execute_task(self):
        # The orchestrator is now clean and easy to read
        name = self._prompt_container_name()
        result = self._send_and_receive(name)
        return result

    def _prompt_container_name(self):
        # Dedicated input handling
        return input("Enter container name: ")

    def _send_and_receive(self, name):
        # Dedicated network logic
        # ... socket setup and transmission ...
        return response

```

---

## Why Cohesive Methods Win

1. **Isolated Testing**: You can now unit test `_prompt_container_name` and `_send_and_receive` independently of the main orchestrator. You can even mock the network method to test your input logic without needing a live server.
2. **Readability**: The `execute_task` method now reads like a table of contents, providing a high-level overview of the entire process without overwhelming the reader with implementation details.
3. **Reuse**: If another feature requires prompting for a container name, you can simply reuse `_prompt_container_name` instead of duplicating the logic.

---

## The Principles of Cohesion

| Principle | Description | Benefit |
| --- | --- | --- |
| **Single Responsibility** | Each method should do exactly one thing. | Easier to name, debug, and replace. |
| **Encapsulation** | Keep implementation details hidden. | Changing network logic doesn't break input logic. |
| **Reduced Coupling** | Orchestrator only knows *that* it happens, not *how*. | High flexibility and low breakage risk. |

---

## Best Practices

* **The "Private" Prefix**: Use the underscore prefix (e.g., `_prompt_container_name`) to signal that these methods are internal implementation details not meant to be called from outside the class.
* **Keep Orchestrators Slim**: If your orchestrator method is longer than 10–15 lines, it is likely doing too much. Extract logic until the orchestrator is just a series of function calls.
* **Refactor by "Pain"**: If you find yourself changing the network logic and worrying about accidentally breaking the input logic, that is a clear sign that the two should be separated.

---

By decomposing your complex methods into small, cohesive sub-methods, you don't just write "better" code—you write code that is modular, flexible, and fundamentally easier to reason about.
