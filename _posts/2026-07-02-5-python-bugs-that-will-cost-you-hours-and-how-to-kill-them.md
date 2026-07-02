---
layout: default
title: "5 Python Bugs That Will Cost You Hours (And How to Kill Them)"
description: "Stop losing time to common Python pitfalls. From mutable defaults to scope leakage, here are 5 bugs that frequently plague developers and the exact architectural fixes to solve them."
---

Author: **Amin Boulouma**, *Software Engineer*
**Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
**Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# 5 Python Bugs That Will Cost You Hours (And How to Kill Them)

Every developer hits the same wall. You write a function, you test it once, and it works. But in production, under load, it behaves erratically. These aren't syntax errors—these are logic traps inherent to how Python handles memory and scoping.

***

### 1. The Mutable Default Argument Trap
We touched on this, but it bears repeating because it is the #1 time-waster. Default arguments are evaluated at **definition time**, not runtime.

* **The Bug:** Using `def func(data=[])`.
* **The Fix:** Always use `data=None` and initialize inside the body.



### 2. The Late Binding Closure
When using loops to create closures (like lambdas), Python binds variables late. All your lambdas will end up using the final value of the loop variable.

* **The Bug:** `funcs = [lambda: i for i in range(3)]` (All will return 2).
* **The Fix:** Use a default argument to capture the value: `lambda i=i: i`.

### 3. Modifying a List While Iterating
Removing items from a list while looping over it skips elements because the index shifts, but the iterator moves forward.

* **The Bug:** `for item in my_list: if cond(item): my_list.remove(item)`.
* **The Fix:** Iterate over a copy: `for item in my_list[:]` or use a list comprehension.

### 4. The "Import Loop" (Circular Imports)
When Module A imports Module B, and Module B imports Module A, Python will crash or return an empty module.

* **The Bug:** Circular dependency chains.
* **The Fix:** Move imports inside the function/method body (local imports) or refactor common logic into a third "base" module.

### 5. Truthiness Confusion (`if x:`)
Beginners often check `if x:` for lists or integers. This evaluates to `False` for an empty list `[]` OR the integer `0`. 

* **The Bug:** `if user_input:` failing when the input is specifically `0`.
* **The Fix:** Be explicit. Use `if x is not None:` or `if len(x) > 0:`.

***

### Complex Example: Resolving Circular Imports
When two modules depend on each other, the cleanest way to break the cycle is by using a shared configuration object or local imports.

```python
# module_a.py
def process_data(data):
    # Local import breaks the circular dependency chain
    from module_b import format_data
    return format_data(data)

# module_b.py
def format_data(data):
    # Business logic here
    return f"Formatted: {data}"

```



### Quick Reference: Bug Fix Guide

| Bug | Symptom | Immediate Fix |
| --- | --- | --- |
| **Mutable Default** | State persists across calls | Use `None` as default |
| **Late Binding** | Closures return last value | Use `val=val` in lambda |
| **List Mutation** | Items skipped in loop | Iterate over `list[:]` |
| **Circular Import** | `ImportError` | Move import inside function |
| **Truthiness** | `0` or `[]` treated as `False` | Use `is not None` |



### Developer Checklist: Is your code robust?

* [ ] **Explicit over implicit:** Are you checking `if x is None` instead of `if not x`?
* [ ] **Memory hygiene:** Are you modifying the same collection you are currently looping through?
* [ ] **Dependency check:** Does your module tree have any bidirectional arrows?
* [ ] **Closure safety:** Are your lambdas capturing loop variables correctly?

### Why we chose these fixes

We prioritize these architectural choices because they create **predictable behavior**. Python's flexibility is a double-edged sword; these patterns force the language into a more rigid, safe state. By handling defaults with `None` and breaking dependencies with local imports, you ensure that your code is not just functional, but also resilient against the "it works on my machine" phenomenon.


### Takeaway

Stop guessing why your code is failing. If you encounter these patterns, refactor immediately. A few minutes of applying these architectural fixes will save you hours of debugging production logs later.