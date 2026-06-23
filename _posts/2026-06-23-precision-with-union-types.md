---
title: Type Safety: Mastering Union Types in Python
description: Learn how to use Union types to improve code clarity and type safety when functions accept multiple data types.
layout: default
---

# Precision with Union Types

As Python’s type hinting system has matured, `Union` types have become an essential tool for expressing that a function or variable can hold one of several different types. By using `Union`, you move away from the ambiguity of "it could be anything" and toward a self-documenting, statically verifiable codebase.

## The Problem: The Ambiguity of `Any`

When a function accepts a parameter that could be either an `int` or a `str`, the lazy approach is to use `Any` or no type hint at all. This forces the reader (and static analysis tools like `mypy`) to guess what the code expects, leading to runtime errors that could have been caught during development.

---

## The Solution: Using `Union`

A `Union` type explicitly defines the set of allowed types. If a value does not match one of these types, your IDE and type checker will flag it immediately.

### Implementation
```python
from typing import Union

def process_id(identifier: Union[int, str]) -> str:
    # Python 3.10+ also supports the pipe syntax: int | str
    return f"Processing ID: {str(identifier)}"

# These are valid
process_id(123)
process_id("abc-456")

# This would trigger a type-checker error
# process_id(None)

```

---

## Modern Syntax: The Pipe Operator (`|`)

In Python 3.10 and newer, the `Union` import is largely optional. You can use the more concise pipe operator (`|`), which is visually clearer and follows standard set notation.

```python
# The modern, cleaner way
def format_input(data: int | str | list[int]) -> str:
    ...

```

---

## When to Use Union Types

1. **Flexible APIs**: Use `Union` when a function is designed to handle multiple common input types, like an ID that can be a numeric index or a unique string slug.
2. **Optional Values**: While `Optional[T]` is the standard for "T or None", `Union[T, None]` is technically identical. Use `| None` for modern, readable code.
3. **Result Normalization**: When a function can return different "shapes" of data (e.g., a `Success` object or an `Error` object), `Union` helps the caller handle those cases explicitly.

---

## Best Practices

* **Exhaustive Matching**: When you return a `Union`, pair it with `match-case` (the structural pattern matching we discussed earlier). This allows you to write code that is guaranteed to handle all possible types defined in your `Union`.
* **Keep Unions Small**: If your `Union` contains more than three or four types, it might be a sign that your function is doing too much. Consider whether you should introduce a common base class or interface instead.
* **Prioritize `|` (Pipe)**: If your project supports Python 3.10+, prefer the pipe operator over `Union[...]`. It is easier to read and requires less boilerplate.

---

By being explicit about the types your code handles, you shift the burden of validation from your runtime logic to your development environment. This leads to fewer bugs and a much better developer experience.

---
