---
layout: default
title: "Why You Should Stop Writing 'Temporary' Code (And What to Do Instead)"
description: "Master the 'Future-Proof' principle: If you plan on deleting it later, don't write it today. Learn how to design systems that are clean from day one."
---

- Author: **Amin Boulouma**, *Software Engineer*
- **Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
- **Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# Why You Should Stop Writing 'Temporary' Code (And What to Do Instead)

Every engineer has been there: you write a "quick fix" or a "temporary migration script" with the firm intention of deleting it in the next sprint. Two years later, that code is still running, it’s integrated into three other services, and nobody dares touch it because it has become "foundational."

**The Problem:** "Temporary" code is rarely temporary. When you write code you plan to delete, you tend to neglect testing, documentation, and decoupling. When that code inevitably persists, it becomes technical debt that compounds interest every day.



### The Glossary
* **Technical Debt:** The "cost" of taking a shortcut now, which you have to pay back later with interest.
* **Refactoring:** Cleaning up code to make it easier to understand and change, without changing what it actually does.
* **Dependency:** When one piece of your code relies on another to work; like a house of cards, if you pull one out, they all might fall.
* **Abstraction:** Hiding complicated details inside a simple box so you don't have to worry about how it works inside.


## Why We Choose Design Over Deletion
We choose to design for longevity because the cost of *deleting* code in a distributed system is much higher than the cost of writing it correctly the first time. If you think you’ll remove it, you are likely missing an abstraction. Instead of writing "temporary" logic, write **pluggable** logic.


## Implementation

### Simple Example: The "Hack" vs. The Pattern
```python
# THE WRONG WAY: Temporary logic that becomes permanent
def process_data(data):
    # This 'if' is a hack we plan to remove later
    if data.get("version") == "legacy":
        return data["old_format"] * 2
    return data["new_format"]

```

### Complex Example: Production-Grade Pluggable Architecture

```python
class DataProcessor:
    """Production-grade: Use a Strategy pattern to isolate 'temporary' variations."""
    def __init__(self, strategy):
        self._strategy = strategy

    def process(self, data):
        return self._strategy.execute(data)

class ModernProcessor:
    def execute(self, data):
        return data["new_format"]

class LegacyProcessor:
    def execute(self, data):
        return data["old_format"] * 2

# Usage: Swap the processor, not the logic inside the method.
# When legacy is gone, we just delete the class, not the main logic flow.
processor = DataProcessor(ModernProcessor())

```


## Quick Reference: Strategy Selection

| Strategy | When to use | Why? |
| --- | --- | --- |
| **Strategy Pattern** | When you expect logic to change | Keeps your main code clean and "deletion-ready." |
| **Feature Flags** | When you are unsure of a feature | Safe way to toggle code without deleting/adding files. |
| **Interfaces/Protocols** | When you have multiple implementations | Decouples implementation from the caller. |


## Developer Checklist

* [ ] Have I created a separate module or class for this "temporary" logic?
* [ ] Is this code covered by a unit test? (If it's not worth testing, it's not worth writing).
* [ ] If I had to delete this tomorrow, would the rest of my system break?
* [ ] Am I using an abstraction that allows me to swap this out later?

### Takeaways

1. **Design for Replaceability:** Always treat your code as if it will be replaced by a better implementation.
2. **Abstract the Change:** If logic is likely to change, isolate it behind an interface.
3. **Delete Promptly:** If you find yourself writing code that is purely temporary, reach for a Feature Flag instead.
