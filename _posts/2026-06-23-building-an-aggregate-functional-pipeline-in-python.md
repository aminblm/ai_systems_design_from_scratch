---
title: Building an Aggregate Functional Pipeline in Python
description: Learn how to transform standard aggregation techniques into a production-ready, multi-stage functional pipeline.
layout: default
---

# Building an Aggregate Functional Pipeline in Python

In data processing, shifting from monolithic aggregate functions to a **multi-stage functional pipeline** significantly improves maintainability, testing, and scalability. By mimicking the structure of database-driven operators like `$match` and `$count`, we can create a clean, declarative data processing flow.

## The Architectural Concept

Instead of nesting functions, we treat each processing step as a discrete unit that accepts and returns a data stream.

### Core Pipeline Structure

A robust pipeline requires:
1.  **Input Source**: The raw data or iterable.
2.  **Operators**: Pure functions performing specific transformations.
3.  **Executor**: A mechanism to chain these operations.

---

## Implementation Example

Below is a Python implementation utilizing functional programming principles. We will implement `match` (filtering) and `count` (aggregation) stages.

```python
from typing import Callable, Iterable, Any, List

def pipeline(data: Iterable[Any], *functions: Callable) -> Any:
    """Executes a series of functions on the data stream."""
    for function in functions:
        data = function(data)
    return data

# Pipeline Stages
def match(predicate: Callable) -> Callable:
    """Filter stage (similar to $match)."""
    return lambda data: filter(predicate, data)

def count() -> Callable:
    """Aggregation stage (similar to $count)."""
    return lambda data: len(list(data))

# Usage
dataset = [10, 25, 40, 55, 70]

# Define the pipeline: Match > 30, then count
result = pipeline(
    dataset,
    match(lambda x: x > 30),
    count()
)

print(f"Pipeline Result: {result}")

```

---

## Key Benefits

* **Modular Design**: Each stage is independently testable.
* **Declarative Syntax**: The code describes *what* to do rather than the internal loop logic of *how* to do it.
* **Extensibility**: You can easily inject new stages (e.g., `project`, `group`, `sort`) without modifying existing logic.

By structuring your processing logic this way, you bridge the gap between simple scripts and professional, pipeline-oriented data engineering architectures.

```

