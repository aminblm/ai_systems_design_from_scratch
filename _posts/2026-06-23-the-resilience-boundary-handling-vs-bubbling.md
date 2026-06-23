---
title: The Resilience Boundary: Try-Except vs. Raising Errors
description: Learn the essential distinction between handling errors locally and bubbling them up in your application architecture.
layout: default
---

# The Resilience Boundary: Handling vs. Bubbling

A common point of confusion in Python development is deciding where to catch an error and where to let it propagate. Understanding this "resilience boundary" is key to writing clean, maintainable systems.

## The Rule of Responsibility

The decision between `try-except` (handling) and `raise` (bubbling) rests on one fundamental question: **"Can this specific layer do something meaningful to recover?"**



---

## When to Use `try-except` (Handle)

Use `try-except` only when you can resolve the issue, provide a fallback, or perform essential cleanup before moving on. 

* **You can provide a default**: If a network request fails, can you load a cached version of the data?
* **You must cleanup**: Even if you can't fix the error, you must release a file lock or close a socket (RAII).
* **You are at the top level**: Your main application loop should catch errors to log them and prevent the entire system from crashing.

```python
try:
    data = fetch_config()
except NetworkError:
    # We can recover by using a local default
    data = load_default_config() 

```

---

## When to Use `raise` (Bubble)

Raise an error (or let it propagate) when you cannot fix the underlying issue. Bubbling errors up is not a failure; it is a way to ensure that the error is handled by a component with enough context to make a correct decision.

* **Missing Context**: A low-level `Git` module shouldn't decide how to display a GUI error message to a user. It should raise the exception.
* **Preventing "Silent Failures"**: If you catch an error but do nothing (e.g., `pass`), you are burying critical bugs.
* **API Integrity**: If your function is passed invalid input, `raise ValueError` immediately. It is better to fail loud and fast than to continue with corrupt state.

```python
def process_git_push(repo):
    if not repo.is_clean():
        # We cannot recover here; bubble up to the caller
        raise GitError("Cannot push: Repo not clean.")

```

---

## The "Translate" Pattern

Sometimes, you need to catch a low-level exception and re-raise a more descriptive, high-level exception. This preserves the error context while hiding internal implementation details.

```python
try:
    db.execute_query()
except SqliteError as e:
    # Translate low-level DB errors to domain-specific errors
    raise DatabaseAccessError("Failed to update user profile") from e

```

---

## Best Practices

| Strategy | When to Apply |
| --- | --- |
| **Handle** | When you have a viable fallback or cleanup task. |
| **Bubble** | When the caller has more context to resolve the issue. |
| **Translate** | When internal errors need to be mapped to public API errors. |

* **Never Use Bare `except**`: Always catch specific exceptions (e.g., `except ConnectionError:`). Bare `except:` clauses hide bugs.
* **Fail Loudly**: If you don't know exactly how to recover, let the exception bubble up. It is easier to debug an unhandled exception than one that was silently swallowed.

---

By being intentional about where you handle errors, you stop writing code that hides problems and start writing code that reports them precisely where they occur.
