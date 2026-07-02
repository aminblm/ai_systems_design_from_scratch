---
layout: default
title: "5 Principles for Clean Code (Without Over-Engineering)"
description: "Why senior engineers prioritize simplicity over clever abstractions. Learn the discipline of writing maintainable, enterprise-grade Python that reads like prose."
---

Author: **Amin Boulouma**, *Software Engineer*
**Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
**Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# 5 Principles for Clean Code (Without Over-Engineering)

Junior engineers often strive for "clever" code, using complex decorators or nested abstractions to save a few lines. Senior engineers strive for **boring code**. If your architecture requires an advanced degree to understand the control flow, you have failed the [Art of Minimalist Engineering](https://aminblm.github.io/ai_systems_design_from_scratch/the-art-of-minimalist-engineering-why-less-code-equals-more-robustness/).

***

### The Problem: The Abstraction Trap
We constantly battle the [Architectural Paradox](https://aminblm.github.io/ai_systems_design_from_scratch/the-architectural-paradox-shell-vs-core/), where we over-engineer the shell while leaving the core logic fragile. Clean code is not about fewer lines; it is about reducing the **cognitive load** required to maintain the system. 



***

### Glossary for Beginners
* **Cohesion:** The degree to which elements inside a module belong together. High cohesion is good.
* **Coupling:** The degree of interdependence between software modules. Low coupling is good.
* **DRY (Don't Repeat Yourself):** A principle to reduce repetition, though it is often misused to create unnecessary abstractions.
* **Refactoring:** The process of restructuring existing code without changing its external behavior.

***

### Why We Choose Simplicity Over Abstraction
When we implement [Modular Design](https://aminblm.github.io/ai_systems_design_from_scratch/cohesive-sub-methods-the-path-to-clean-orchestration/), we prioritize readability. If you find yourself building a [Facade Pattern](https://aminblm.github.io/ai_systems_design_from_scratch/the-facade-design-pattern/), ask yourself: am I hiding complexity, or am I just moving it to another file? Avoid [Redundant Abstractions](https://aminblm.github.io/ai_systems_design_from_scratch/redundant-abstractions-flattening-the-pipeline/).

***

### Implementation: Cohesive Methods
Instead of a single "God-Method" that handles parsing, validation, and rendering, break it down. Clean code is composed of functions that do **one thing**.

```python
class DataProcessor:
    """
    Cohesive methods make the control flow explicit.
    """
    def run(self, raw_input):
        # The orchestrator is readable because logic is delegated
        validated = self._validate(raw_input)
        transformed = self._transform(validated)
        return self._save(transformed)

    def _validate(self, data): ...
    def _transform(self, data): ...
    def _save(self, data): ...

```

### Complex Example: Defeating the Pyramids of Doom

Deep nesting is the enemy of maintenance. We use [Structural Pattern Matching](https://aminblm.github.io/ai_systems_design_from_scratch/mastering-pythons-match-case-structural-pattern-matching/) to flatten our logic.

```python
def handle_event(event):
    # Pattern matching flattens logic, removing deep nesting
    match event:
        case {"type": "click", "id": id}:
            return f"Clicked {id}"
        case {"type": "hover", "id": id}:
            return f"Hovered {id}"
        case _:
            raise ValueError("Unknown event")

```



### Quick Reference: Clean Code Heuristics

| Principle | Antipattern | Fix |
| --- | --- | --- |
| **Cohesion** | God-Method | Break into private helpers |
| **Readability** | Magic Numbers | Define named constants |
| **Naming** | `data`, `obj`, `val` | Use domain-specific terminology |
| **Logic** | Deep Nesting | Early returns or pattern matching |



### Developer Checklist: Is your code clean?

* [ ] **Single Responsibility:** Does this function do exactly one thing?
* [ ] **Encapsulation:** Are my internal state changes hidden behind [Strict Encapsulation](https://aminblm.github.io/ai_systems_design_from_scratch/5-hidden-benefits-of-strict-encapsulation-without-breaking-your-architecture/)?
* [ ] **Type Safety:** Am I using [ParamSpec and TypeVar](https://aminblm.github.io/ai_systems_design_from_scratch/paramspec-and-typevar-the-architecture-of-type-safe-wrappers/) to enforce contracts?
* [ ] **Simplicity:** Can I explain this function to a junior engineer in under two minutes?

### Takeaway

Writing better code is an exercise in empathy—empathy for the engineer who will maintain your work six months from now. Stop [Over-Engineering](https://aminblm.github.io/ai_systems_design_from_scratch/the-silent-killer-over-engineering/) and start prioritizing [Cohesive Orchestration](https://aminblm.github.io/ai_systems_design_from_scratch/cohesive-sub-methods-the-path-to-clean-orchestration/). The best code is code that doesn't need to be explained.
