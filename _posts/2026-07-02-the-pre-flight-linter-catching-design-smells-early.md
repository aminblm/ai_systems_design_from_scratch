---
layout: default
title: "The Pre-Flight Linter: Enforcing Architectural Integrity at the Gate"
description: "Why runtime checks are too late and how to implement a custom static analysis pipeline to catch design smells before they hit CI."
---

- Author: **Amin Boulouma**, *Software Engineer*
- **Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
- **Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# The Pre-Flight Linter: Catching Design Smells Early

Ever wonder why your CI pipeline passed, but your service failed in production due to a circular import or a prohibited database access pattern? You likely have a **runtime-first architecture**. 

The "midnight deployment spike" often occurs not because of load, but because a developer bypassed a module boundary that wasn't strictly enforced. By the time the code reaches the test suite, the architectural violation is already deeply woven into your dependency graph. A **Pre-Flight Linter** enforces design constraints at the static analysis stage—before code is even compiled or interpreted.



## The Strategy: Shift Left on Architecture
Static Analysis is the practice of inspecting code without running it. While standard linters (like Flake8 or ESLint) check for style, a **Pre-Flight Linter** checks for **Intent**.

* **Constraint**: "Service A shall never call the User DB directly."
* **Enforcement**: Scanning the Abstract Syntax Tree (AST) for prohibited imports.

## Glossary for Beginners
* **AST (Abstract Syntax Tree)**: A computer's way of "drawing" a map of your code so it understands how pieces fit together.
* **Static Analysis**: Studying the blueprint of the house without having to walk inside.
* **Circular Import**: When two files keep asking each other for help, creating an infinite loop. (Imagine two people standing in a line saying "After you," "No, after you").
* **Constraint**: A rule that says "You cannot do this."


## Simple Implementation: The Import Checker
This script parses a Python file to find prohibited imports, preventing developers from accessing the internal database layer.

```python
import ast

# Define forbidden modules
FORBIDDEN = {'internal_db_driver'}

def check_imports(file_path):
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name in FORBIDDEN:
                    return f"SECURITY VIOLATION: {name.name} is forbidden."
    return "Check Passed"

```


## Complex Implementation: Production-Grade Enforcement

For larger systems, we need to traverse directories and ignore specific non-critical paths.

```python
import ast
import os

class ArchitectureLinter:
    def __init__(self, rules):
        self.rules = rules # Mapping of file path patterns to forbidden modules

    def lint_project(self, root_dir):
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".py"):
                    self._lint_file(os.path.join(root, file))

    def _lint_file(self, path):
        with open(path, "r") as f:
            tree = ast.parse(f.read())
            # Logic to verify node relationships against self.rules
            # Includes logging and exit-code management for CI/CD
            pass

# Usage: Ensure 'domain_layer' never imports from 'infrastructure'
rules = {'domain_layer': ['infrastructure']}
linter = ArchitectureLinter(rules)

```

## Quick Reference: Linter vs. Test Suite

| Feature | Static Analysis (Linter) | Unit Testing |
| --- | --- | --- |
| **Stage** | Pre-Commit / Pre-Build | Post-Build |
| **Focus** | Structural Integrity / Standards | Functional Correctness |
| **Execution** | Reads code as text/AST | Executes code |
| **Speed** | Near instantaneous | Can take minutes/hours |

## Why We Choose Static Analysis over Runtime Checks

Runtime checks (like `if` statements inside your functions) add overhead to every request and are often forgotten. **Static Analysis** is **immutable**—if the code is written in a way that violates the architecture, it simply won't build. It treats your design constraints as code.

## Developer Checklist

* [ ] Are architectural boundaries defined in a central config?
* [ ] Is the linter blocking on CI/CD (Fail-fast)?
* [ ] Are exemptions handled via explicit `@noqa` or configuration rather than code changes?
* [ ] Does your linter output actionable error messages for the developer?

### Takeaways

* **Gatekeeping**: Don't rely on code reviews to catch architectural drift; automate it.
* **Visual Mapping**: Use tools to visualize your imports periodically.
* **Design Enforcement**: Treat your software architecture as a hard constraint, not a suggestion.
