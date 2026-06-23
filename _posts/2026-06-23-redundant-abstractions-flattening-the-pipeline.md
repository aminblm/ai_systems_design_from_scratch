---
title: Defeating Redundant Abstraction: Simplifying Your Pipeline
description: Learn to recognize and eliminate "layering rot" by flattening redundant classes and simplifying your data transformation pipelines.
layout: default
---

# Redundant Abstractions: Flattening the Pipeline

In software engineering, we often feel that "more classes mean better design." However, when you see a pipeline containing `MarkdownToHTMLBuilder`, `MarkdownToHTML`, and `HTMLGenerator`, you aren't looking at "clean design"—you are looking at **Redundant Abstraction**.

These layers exist as a web of dependencies, forcing the developer to track state and data passing through multiple wrappers that provide no actual benefit. This is a classic case of **"layering rot"**—where the architecture becomes a burden to the task it is supposed to perform.

## The Problem: Cognitive Overload
A simple pipeline—transforming text into HTML—should be straightforward. When you add three layers of indirection, you force anyone reading the code to hold the entire "web of dependencies" in their head just to trace a single string transformation.



### Why It Fails
* **Opaque Data Flow**: It is unclear which class is responsible for the actual transformation logic.
* **Maintenance Tax**: If the parsing requirement changes, you have to propagate that change through three different class interfaces.
* **Performance Overhead**: Frequent object instantiation and string copying across layers degrade performance without adding value.

---

## The Solution: Flattening for Clarity

The best way to fix redundant abstraction is to ask: *If I delete these intermediate classes, does the code become more or less understandable?* Usually, the answer is "more."

### From Complex Web to Lean Pipeline
```python
# Instead of: builder -> converter -> generator
# Use a simple, linear function:
def markdown_to_html(markdown_text: str) -> str:
    # 1. Parse
    parsed_data = parse_markdown(markdown_text)
    # 2. Transform
    html = transform_to_html(parsed_data)
    return html

```

---

## How to Spot Redundant Abstractions

| Symptom | The "Clean" Reality |
| --- | --- |
| **Pass-through Classes** | Classes that only call one method in another class. |
| **"Manager" or "Builder" Suffixes** | Classes that don't actually manage state or build complex objects. |
| **Deep Dependency Webs** | Functions that call functions, rather than classes calling classes. |
| **Fragmented Logic** | Logic for a single task spread across 5+ files. |

---

## Best Practices

* **The "Delete Test"**: If you can inline a class's logic into the calling function without breaking the interface, do it.
* **Prefer Functions for Transforms**: If your task is a pure data transformation (Text -> HTML), a function is almost always better than a class. Classes are for managing state; functions are for processing data.
* **Embrace Minimalism**: Your architecture should only be as complex as the problem it solves. If your pipeline is just a simple transformation, your code should reflect that simplicity.

---

Complexity is the enemy of maintainability. By stripping away these redundant abstractions, you turn an opaque "web" of code into a transparent, linear pipeline that is easy to read, test, and evolve.
