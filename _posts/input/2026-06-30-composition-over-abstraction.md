---
title: "Composition over Abstraction: Why Pipelines Win"
description: "Exploring the power of function composition through Python's functional programming patterns."
layout: default
---

# Composition over Abstraction

The code snippet `IOUtility.text_to_lines_generator(IOUtility.read_decoded(file_path))` is a classic example of **function composition**. Instead of creating a complex "God Object" or a deeply nested class hierarchy (over-abstraction), you are piping data through small, focused, and reusable functions.

## The Concept: Composition vs. Abstraction

* **Abstraction** often involves hiding complexity behind interfaces or classes, which can lead to "abstraction bloat"—where you spend more time managing the structure than the data.
* **Composition** is the act of combining simple, distinct functions to create more complex logic. By passing the output of one function directly into the input of another, you keep your logic modular and testable.



## Analyzing Your Pattern

Your snippet is a perfect example of a **data pipeline**. 

```python
# The Nested Approach (Harder to read as it grows)
result = IOUtility.text_to_lines_generator(IOUtility.read_decoded(file_path))

# The Composed Approach (More readable for complex pipelines)
raw_data = IOUtility.read_decoded(file_path)
lines = IOUtility.text_to_lines_generator(raw_data)

```

### Why this is superior to heavy abstraction:

1. **Loose Coupling:** Each function is agnostic of the other. `text_to_lines_generator` doesn't care *where* the text came from, only that it is a string.
2. **Testability:** You can unit test `read_decoded` and `text_to_lines_generator` in isolation.
3. **Flexibility:** If you want to change how you read files (e.g., adding encryption), you only change the first function in the chain, not the entire pipeline architecture.

## Visualizing the Pipeline

In a composition-heavy architecture, you view your system as a series of transformations:

## When to prioritize Composition

* **Data Processing:** Any task involving ETL (Extract, Transform, Load) or streams.
* **Middleware:** Request/Response cycles in web frameworks.
* **Utility Libraries:** When functions don't need to hold "state."

By avoiding excessive abstraction—such as creating an `FileProcessor` class that holds internal state—and favoring functional composition, you ensure your code remains agile and easy to debug.
