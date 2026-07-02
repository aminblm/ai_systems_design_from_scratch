---
layout: default
title: "The Ultimate Guide to Python Argument Specifiers (Without the Confusion)"
description: "Why you see '/', '*', and '...' in Python function signatures, and how they force strict API design."
---

- Author: **Amin Boulouma**, *Software Engineer*
- **Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
- **Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# The Ultimate Guide to Python Argument Specifiers (Without the Confusion)

When exploring modern Python type-hinting or enterprise-grade libraries, you’ve likely stumbled upon syntax that looks like cryptic punctuation: `def func(a, /, b, *, c)`. It’s not a typo, and it’s not just for stylistic preference. These are **Positional-Only** and **Keyword-Only** argument specifiers.

**The Problem:** In large systems, if a library author renames an argument, it can break every client's code that calls that function by keyword. Developers struggle because they don't know which arguments are safe to pass by name and which are "private" to the implementation. This leads to brittle APIs and unnecessary bugs during refactoring.



### The Glossary (5-Year-Old Edition)
* **Argument:** The input you give to a machine to start it up.
* **Positional-Only (/):** Arguments you must hand to the machine in a specific order, like putting ingredients in a bowl.
* **Keyword-Only (*):** Arguments you must label, like putting a sticky note on a gift so the person knows what it is.
* **Ellipsis (...):** A "placeholder" dot that means "I'll fill this in later" or "nothing to see here yet."


## Why We Choose Strict Argument Specifiers Over Flexible Signatures
We choose these specifiers to enforce **API Stability**. By marking arguments as `/` (Positional-Only), we tell the user: "The name of this argument is internal; don't rely on it." This gives us the freedom to rename `address` to `dest` in future versions without breaking your production code.


## Implementation

### Simple Example: Forcing Order
```python
def connect(address: str, /):
    # The '/' means 'address' must be passed positionally
    print(f"Connecting to {address}")

# connect(address="127.0.0.1")  # THIS WILL RAISE A TYPE ERROR
connect("127.0.0.1")            # This is the only valid way

```

### Complex Example: Production-Grade Signature

```python
class ConnectionManager:
    def __init__(self, /, host: str, *, timeout: int = 30, retries: int = 3):
        # host: Positional-Only (internal name doesn't matter)
        # timeout, retries: Keyword-Only (must be explicit for clarity)
        self.host = host
        self.timeout = timeout
        self.retries = retries

    def execute(self, command: str, /) -> None:
        """
        ... denotes an omitted implementation in a stub or protocol.
        """
        ... 

# Usage:
# mgr = ConnectionManager("localhost", timeout=10) # Clean, explicit API

```


## Quick Reference: Strategy Selection

| Symbol | Meaning | Best Use Case |
| --- | --- | --- |
| **/** | Positional-Only | Internal library arguments that may change. |
| ***** | Keyword-Only | Boolean flags or optional configuration. |
| **...** | Ellipsis (Stub) | Interfaces/Protocols where logic is not implemented. |


## Developer Checklist

* [ ] Is my public API designed to survive future refactors?
* [ ] Are optional parameters forced into `Keyword-Only` to prevent confusion?
* [ ] Did I use `...` for base class methods that must be overridden?
* [ ] Is my signature readable at a glance?

### Takeaways

1. **Name Stability:** Use Positional-Only (`/`) to protect your implementation details.
2. **Explicit is Better than Implicit:** Use Keyword-Only (`*`) for any argument that changes behavior.
3. **Stubs for Interfaces:** Use `...` when defining the contract, not the behavior.

**Counter-intuitive insight:** The most maintainable code is often the code that forbids flexibility. By restricting how your functions can be called, you provide a clear, unambiguous contract that saves your team hours of debugging during future migrations.
