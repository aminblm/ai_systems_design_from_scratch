---
title: "Mastering Reverse Iterators in Python"
description: "How to efficiently traverse sequences in reverse using built-in Python tools."
layout: default
---

# Reverse Iterators: Traversing Backwards

In Python, a reverse iterator is an object that allows you to traverse a sequence from the last element to the first. While you could index backwards using negative numbers (e.g., `list[-1]`), using a dedicated reverse iterator is more memory-efficient and idiomatic.

## The `reversed()` Built-in
The most common way to create a reverse iterator is using the `reversed()` function. It takes any sequence—like a list, tuple, or range—and returns an iterator that yields elements in reverse order without duplicating the sequence in memory.



## How It Works
Unlike `list.reverse()`, which modifies the original list in place, `reversed()` returns a new iterator object. This is a crucial distinction for functional programming and memory management.

```python
# The idiomatic way to reverse a list
data = [1, 2, 3, 4]

# Returns an iterator, does not copy the list
for item in reversed(data):
    print(item) # Output: 4, 3, 2, 1

```

## Creating Your Own: `__reversed__`

If you are building custom classes, you can enable reverse iteration by implementing the `__reversed__` magic method. This allows your objects to work seamlessly with the `reversed()` function.

```python
class MySequence:
    def __init__(self, data):
        self.data = data
    
    def __reversed__(self):
        return iter(self.data[::-1])

# Usage
obj = MySequence([10, 20, 30])
for item in reversed(obj):
    print(item)

```

## Comparison: Slicing vs. `reversed()`

| Feature | Slicing `[::-1]` | `reversed()` |
| --- | --- | --- |
| **Memory** | Creates a copy of the sequence | Iterates without copying |
| **Type** | Returns a new list/sequence | Returns an iterator |
| **Efficiency** | Lower (due to memory allocation) | Higher (lazy evaluation) |

## Best Practices

1. **Prefer `reversed()` for large datasets:** Because it yields elements one by one, it is significantly more memory-efficient for large lists or custom sequences.
2. **Use Slicing for small lists:** If you specifically need a new list in reverse order (and the data is small), slicing `[::-1]` is often more readable.
3. **Check for `__reversed__`:** If you are consuming unknown objects, always check if they implement the reverse protocol before attempting to manually reverse them.
