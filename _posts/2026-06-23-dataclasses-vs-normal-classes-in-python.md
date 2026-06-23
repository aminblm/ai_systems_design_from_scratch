---


title: "Dataclasses vs. Normal Classes in Python"
description: "Discover why dataclasses have become the modern standard for data-centric objects and how they improve code safety."
layout: default


---


<head>
  <meta charset="utf-8">
  <title>{{ page.title }} | {{ site.title }}</title>
  <meta name="description" content="{{ page.description | default: site.description }}">
  <link rel="canonical" href="{{ site.url }}{{ site.baseurl }}{{ page.url }}">
  
  <meta property="og:type" content="article">
  <meta property="og:title" content="{{ page.title }}">
  <meta property="og:description" content="{{ page.description | default: site.description }}">
  <meta property="og:url" content="{{ site.url }}{{ site.baseurl }}{{ page.url }}">
  <meta property="og:site_name" content="{{ site.title }}">
  
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{{ page.title }}">
  <meta name="twitter:description" content="{{ page.description | default: site.description }}">
</head>

{% raw %}

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>


<div style="text-align: center; margin: 2rem 0; padding-bottom: 1rem; border-bottom: 1px solid #e9ebec;">
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">🏠 Documentation Hub</a>
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/blog" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">📝 Engineering Blog</a>
  <a href="https://github.com/aminblm/ai_systems_design_from_scratch" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">💻 GitHub Repository</a>
</div>

{% endraw %}



# Dataclasses vs. Normal Classes in Python

<div class="author-card">
    <p><strong>{{ site.author.name }}</strong> — <i>{{ site.author.bio }}</i></p>
</div>


In modern Python development, the `dataclass` decorator (introduced in Python 3.7) has revolutionized how we handle objects that primarily exist to store data. Moving away from manual `__init__` boilerplate and error-prone attribute assignments is a critical step toward writing cleaner, more professional code.

## The Problem: The Boilerplate Tax

Standard classes often require repetitive code just to initialize attributes. This creates surface area for bugs—such as typos in variable names or inconsistent initializations.

### The Old Way (Standard Class)
```python
class User:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"User(name={self.name}, age={self.age})"

```

## The Modern Way: Dataclasses

Dataclasses leverage **native type hinting** to generate common methods (`__init__`, `__repr__`, `__eq__`) automatically, reducing your class definition to its core schema.

### The Idiomatic Solution

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    email: str

# Usage
user = User("Alice", 30, "alice@example.com")
print(user)

```

### Why Dataclasses are Superior

1. **Reduced Boilerplate**: You no longer need to write manual assignments.
2. **Type Hinting Integration**: Because they rely on type hints, static analysis tools (like `mypy` or `pyright`) can catch bugs before you even run your code.
3. **Built-in Comparison**: By default, dataclasses include an `__eq__` method that compares the actual data values, not just the object identity in memory.
4. **Immutability**: By adding `@dataclass(frozen=True)`, you can easily create immutable data structures, which are safer in multi-threaded or complex state-management environments.

## Comparison at a Glance

| Feature | Standard Class | Dataclass |
| --- | --- | --- |
| **Initialization** | Manual (`__init__`) | Automatic |
| **Representation** | Manual (`__repr__`) | Automatic |
| **Comparison** | Manual (`__eq__`) | Automatic |
| **Type Safety** | Optional/Loose | Native/Strict |
| **Verbosity** | High | Low |

## When to Stick with Standard Classes

Dataclasses are specifically for **data-centric objects**. You should continue using standard classes when:

* The object requires complex internal logic inside `__init__` (e.g., resource connection).
* The object represents a service or a controller, not a data structure.
* You need private attributes or custom property setters that require more control than basic field assignment provides.

## Final Best Practice

Always treat your data objects as schemas. Using dataclasses with type hints turns your data structures into self-documenting contracts, making it significantly easier for your team to understand exactly what data a method expects and returns.

{% raw %}


<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

{% endraw %}

