---
layout: default
title: "collections.abc vs. typing: Choosing the Right Tool for Python Type Introspection"
description: "Master the distinction between runtime ABCs and static typing definitions to write cleaner, more efficient, and type-safe Python code."
---

- Author: **Amin Boulouma**, *Software Engineer*
- **Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
- **Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# collections.abc vs. typing: The Architectural Divide

In enterprise Python, a common point of confusion is when to use `collections.abc` and when to use `typing`. This confusion often leads to "leaky abstractions" where runtime logic is mixed with static analysis metadata, causing the "midnight deployment spike"—where an application fails because an imported type wasn't available in the runtime environment.

Understanding the boundary between these two is critical for building **resilient, minimalist systems**.



## The Theory: Runtime vs. Build-Time
* **`collections.abc`**: These are **Runtime Abstract Base Classes**. They exist while your code is running and are used for `isinstance()` checks and structural inheritance.
* **`typing`**: This is a **Static Analysis Library**. These types exist primarily for your IDE, MyPy, and Pyright to catch bugs *before* your code ever runs.

## Glossary for Beginners
* **Introspection**: The ability of a program to examine its own types or properties while it is running.
* **Runtime**: The exact moment your code is executing on the server.
* **Static Analysis**: The "pre-flight" check performed by tools to find bugs without executing the code.
* **ABC (Abstract Base Class)**: A template that defines what a class *must* do, without defining how it does it.

---

## Simple Implementation: Runtime Checking
When you need to verify if an object is an iterable at runtime, `collections.abc` is your tool.

```python
from collections.abc import Iterable

def process_data(data):
    # Runtime check: Does this object support iteration?
    if not isinstance(data, Iterable):
        raise TypeError("Expected an iterable object")
    
    for item in data:
        print(item)

```

---

## Complex Implementation: Static Type Hinting

When you want your IDE to warn you if you pass a list to a function expecting a dictionary, use `typing`.

```python
from typing import Mapping, TypeVar

T = TypeVar("T")

# Static check: MyPy verifies the interface before deployment
def update_config(config: Mapping[str, T]) -> None:
    # Logic implementation...
    pass

```

## Quick Reference: When to use which?

| Use Case | `collections.abc` | `typing` |
| --- | --- | --- |
| **`isinstance()` checks** | Yes | No |
| **`issubclass()` checks** | Yes | No |
| **Static Linter Hints** | Limited | Yes |
| **Defining Protocol** | Best for runtime behavior | Best for structural verification |

## Why We Choose `collections.abc` for Minimalist Architecture

In the Starlette codebase, you see a heavy reliance on `collections.abc`. We choose this because it keeps our code **lightweight and runtime-native**. By relying on standard ABCs, we avoid the overhead of the `typing` module in our hot execution paths. We use `typing` solely as an "overlay" for the static analysis tools, ensuring our runtime remains pure and fast.

## Developer Checklist

* [ ] Are you performing runtime type validation using `collections.abc`?
* [ ] Are you keeping your `typing` imports inside `if TYPE_CHECKING:` blocks for maximum performance?
* [ ] Have you replaced deprecated `typing` generics (e.g., `typing.List`) with standard built-ins (e.g., `list`) in Python 3.9+?
* [ ] Is your logic decoupled from type-hinting imports to prevent circular dependencies?

### Takeaways

* **Runtime Integrity**: Use `collections.abc` to ensure your objects behave correctly while the service is live.
* **Static Safety**: Use `typing` to ensure your team's code follows the architectural contracts you've designed.
* **Minimalism**: Don't import from `typing` if you don't need to; Python's standard types are becoming increasingly expressive.
