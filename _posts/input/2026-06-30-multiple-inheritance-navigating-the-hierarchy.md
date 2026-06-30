---
title: "Mastering Multiple Inheritance and MRO in Python"
description: "A guide to understanding how Python resolves method calls in complex inheritance hierarchies using the C3 linearization algorithm."
layout: default
---

# Multiple Inheritance: Navigating the Hierarchy

In Python, multiple inheritance allows a class to inherit features from several parent classes. While powerful, it introduces complexity in determining which version of a method is executed when multiple parents define the same name.

## The C3 Linearization Algorithm
Python resolves the "Method Resolution Order" (MRO) using the **C3 linearization algorithm**. It ensures that:
1. Children are visited before parents.
2. Parent order in the class definition is respected.
3. Monotonicity is maintained (the order is consistent across the hierarchy).



## Analyzing your Hierarchy: `LabServerApp`

When you define a class like this:
```python
class LabServerApp(ExtensionAppJinjaMixin, LabConfig, ExtensionApp):
    pass

```

The order is explicit. Python inspects the classes from left to right. If a method is not found in the child, it searches `ExtensionAppJinjaMixin` first, then `LabConfig`, and finally `ExtensionApp`.

### The MRO Trap

A common misconception is that the "last" parent takes precedence. In reality, the **first** parent (the leftmost one) has the highest priority in the MRO.

## Essential Tools for Debugging

When dealing with deep inheritance, never guess the resolution order. Use these built-in tools:

* **`ClassName.mro()`**: Returns a list of classes in the order they will be searched.
* **`ClassName.__mro__`**: A tuple attribute containing the same resolution sequence.

```python
# Always check your work when using multiple inheritance
print(LabServerApp.mro())

```

## Best Practices

1. **Minimize Depth:** Deep, multi-branched inheritance is notoriously difficult to debug. If you find yourself going deeper than two levels, consider **Composition** instead.
2. **Use `super()` wisely:** `super()` in Python does not just call the "parent." It calls the next class in the **MRO**. This makes it safer for multiple inheritance because it ensures the entire chain is traversed correctly.
3. **Favor Mixins:** Use classes designed as "Mixins" (like your `ExtensionAppJinjaMixin`) to add specific, independent behaviors rather than creating a tangled web of dependencies.

## Summary Checklist

* **Order matters:** The leftmost class in your definition is the first one checked.
* **Inspect often:** Use `.__mro__` to verify your assumptions during development.
* **Super is your friend:** When overriding methods in a multi-inheritance scenario, always call `super()` to ensure the MRO chain continues as intended.
