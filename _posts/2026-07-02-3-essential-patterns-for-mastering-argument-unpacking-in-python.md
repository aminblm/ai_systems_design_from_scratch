---
layout: default
title: "3 Essential Patterns for Mastering Argument Unpacking in Python"
description: "Unlock the power of *args and **kwargs to write cleaner, more flexible, and highly reusable Python interfaces."
---

Author: **Amin Boulouma**, *Software Engineer*
**Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
**Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# 3 Essential Patterns for Mastering Argument Unpacking in Python

In Python development, building flexible interfaces is a core requirement for enterprise-grade systems. How do you create a function that handles an arbitrary number of inputs? Or pass dynamic configurations from one module to another? The answer lies in **Argument Unpacking**—the use of the `*` (splat) and `**` operators.

***

### The Core Concept
Argument unpacking allows you to transform collections (lists, tuples) into positional arguments, or dictionaries into keyword arguments. It acts as a bridge between a collection of data and a function's signature.



#### Glossary for Beginners
* **Positional Arguments:** Arguments that need to be included in the proper order in a function call.
* **Keyword Arguments:** Arguments passed to a function that are preceded by an identifier (e.g., `key=value`).
* **Splat Operator (`*`):** Used to unpack an iterable (like a list or tuple) into individual positional arguments.
* **Double Splat Operator (`**`):** Used to unpack a dictionary into individual keyword arguments.

***

### Why We Choose Unpacking over Hard-Coding
We choose unpacking to implement **Decorator patterns** and **Proxy wrappers**. When building middleware—like a logger or a validator—we don't always know the exact signature of the target function. Unpacking allows our middleware to pass data through without needing to know the specific structure, drastically reducing code coupling.

**Why X over Y?** We use unpacking instead of passing a single `data_dict` object because unpacking preserves the original function signature, allowing static analysis tools (like `mypy`) to maintain better visibility into the data being processed.

***

### Implementation: The Unpacking Pattern

#### Simple Example: Flexible Function Calls
```python
def configure_network(host: str, port: int, timeout: int) -> None:
    print(f"Connecting to {host}:{port} with {timeout}s timeout")

# Unpacking a list and a dictionary
settings = ["127.0.0.1", 8080]
params = {"timeout": 30}

configure_network(*settings, **params)

```

#### Complex Example: Building a Generic Wrapper

In production, we use unpacking to create generic retry logic that works on any function regardless of its signature.

```python
from typing import Callable, Any

def retry_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            # Unpack everything we received into the original function
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Retrying due to: {e}")
            return func(*args, **kwargs)
    return wrapper

@retry_decorator
def api_call(endpoint: str, retries: int = 3) -> str:
    return f"Success at {endpoint}"

# Usage
print(api_call("[https://api.service.com](https://api.service.com)", retries=5))

```



### Quick Reference: Unpacking Strategies

| Pattern | Use Case | Mechanism |
| --- | --- | --- |
| **`*args`** | Positional collection | Unpacks iterables into sequence |
| **`**kwargs`** | Keyword configuration | Unpacks dicts into key-value pairs |
| **`func(*d, **k)`** | Proxy/Wrapper | Maintains original interface |


### Developer Checklist

* [ ] Are you using `*args` and `kwargs` for actual flexible needs, or is it masking poor API design?
* [ ] Does your wrapper function correctly return the result of the unpacked call?
* [ ] Have you verified that argument names in your dictionary match the target function's keywords?
* [ ] Are you using type hints (e.g., `*args: Any`) to maintain clarity in the wrapper?

### TL;DR Summary

Use `*` and `` to make your code **future-proof**. By mastering unpacking, you create wrappers that are agnostic to the specific data they handle, which is the key to building decoupled, enterprise-grade architectures. If you can define the signature explicitly, do so—but when you can't, unpack with confidence.
