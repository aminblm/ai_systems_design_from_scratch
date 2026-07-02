---
layout: default
title: "Typing Protocol: Structural Typing for Decoupled Python Architectures"
description: "Learn how to use Python's Protocol class to enforce structural interfaces, enabling true dependency inversion without heavy inheritance."
---

- Author: **Amin Boulouma**, *Software Engineer*
- **Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
- **Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# Protocol: The Power of Structural Typing

In large enterprise systems, traditional inheritance-based interfaces (ABCs) create rigid, brittle hierarchies. If you want to use a module that wasn't built for your system, you are forced to refactor it to inherit from your base classes. This tight coupling is a primary driver of the "midnight deployment spike"—unforeseen side effects caused by deep inheritance chains.

**`typing.Protocol`** solves this by implementing **Structural Typing** (often called "Duck Typing" in the dynamic world). Instead of checking *what an object is*, the system checks *what an object can do*.



## The Theory: Nominal vs. Structural
* **Nominal Typing (Inheritance)**: "I am a `Database` because I say `class MyDB(Database)`."
* **Structural Typing (Protocol)**: "I am a `Database` because I have a `connect()` method and a `query()` method, regardless of where I came from."

This allows your code to interact with any object that meets your interface requirements, even if the objects share no common ancestor.

## Glossary for Beginners
* **Protocol**: A definition of the minimum "behaviors" (methods or attributes) an object must have to be considered a certain type.
* **Structural Typing**: Checking if an object "looks" or "acts" like a specific type by inspecting its structure.
* **Duck Typing**: "If it walks like a duck and quacks like a duck, it's a duck."
* **Coupling**: How much two parts of your system depend on each other. (Protocols minimize this).


## Simple Implementation: Defining an Interface
You define a `Protocol` to tell your system what you expect, without forcing objects to inherit from it.

```python
from typing import Protocol

class Schedulable(Protocol):
    def run(self) -> None:
        ...

def start_job(job: Schedulable):
    job.run()

# Any class with a 'run' method will now pass type-checking automatically.

```


## Complex Implementation: Production-Grade Service Contracts

In a production-grade microservice, you can use Protocols to define contracts between services. If a service satisfies the protocol, it can be swapped out instantly without modifying the orchestrator code.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class DataProvider(Protocol):
    async def get_data(self, key: str) -> dict: ...

class CacheService:
    async def get_data(self, key: str) -> dict:
        return {"data": "cached"}

# The Orchestrator doesn't care about the implementation, only the behavior
async def sync_service(provider: DataProvider):
    data = await provider.get_data("id_001")
    return data

```

## Quick Reference: Inheritance vs. Protocol

| Feature | Abstract Base Class (ABC) | Typing Protocol |
| --- | --- | --- |
| **Coupling** | High (Hard dependency) | Low (Implicit compatibility) |
| **Flexibility** | Rigid | Extremely High |
| **Design Intent** | Explicit Inheritance | Implicit Contract |
| **Verification** | Runtime (`isinstance`) | Static (MyPy/Pyright) |

## Why We Choose Protocol over ABCs

We choose **Protocol** to achieve **Dependency Inversion**. It allows us to define our system's needs in the core business logic while letting individual modules implement those needs at their own pace, without ever needing to import the core definitions. This eliminates the "dependency hell" where changing one base class forces a rebuild of 50 dependent modules.

## Developer Checklist

* [ ] Are you using `Protocol` instead of inheritance for interface definitions?
* [ ] Have you added `@runtime_checkable` if you need to perform `isinstance()` checks at runtime?
* [ ] Are your protocols kept small and focused (Single Responsibility Principle)?
* [ ] Do your static analysis tools (MyPy) show the protocol as satisfied?

### Takeaways

* **Design for Behavior**: Define what your system *needs* to do, not what the classes *should be*.
* **Decouple**: Use Protocols to bridge independent modules without creating a shared inheritance tree.
* **Flexibility**: Protocols allow you to adopt 3rd-party libraries into your system architecture without refactoring their code to match your hierarchy.
