---

title: "Understanding Class Methods vs. Static Methods in Python"
description: "A deep dive into the differences, use cases, and syntax of class methods and static methods in Python."
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


<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>


<a href="https://www.producthunt.com/products/ai-systems-design-from-first-principles?embed=true&amp;utm_source=badge-featured&amp;utm_medium=badge&amp;utm_campaign=badge-ai-systems-design-from-first-principles" target="_blank" rel="noopener noreferrer"><img alt="AI Systems Design From First Principles - An implementation of AI Systems Design From First Principles | Product Hunt" width="250" height="54" src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1173628&amp;theme=dark&amp;t=1781635927239"></a>

{% raw %}

<div style="text-align: center; margin: 2rem 0; padding-bottom: 1rem; border-bottom: 1px solid #e9ebec;">
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">🏠 Documentation Hub</a>
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/blog" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">📝 Engineering Blog</a>
  <a href="https://github.com/aminblm/ai_systems_design_from_scratch" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">💻 GitHub Repository</a>
</div>

{% endraw %}


# Class Methods vs. Static Methods in Python

{% raw %}

<div class="author-card">
    <p><strong>Amin Boulouma</strong>, <i>Software Engineer</i></p>
</div>

{% endraw %}



In Python, understanding the difference between `classmethod` and `staticmethod` is crucial for writing clean, object-oriented code. While both are decorators used to define methods that don't necessarily behave like standard instance methods, they serve very different purposes.

## The Standard Instance Method
Before diving into the decorators, remember that a standard method (defined without a decorator) receives the instance (`self`) as its first argument.

```python
class MyClass:
    def instance_method(self):
        print(f"I belong to instance: {self}")

```

## What is a Class Method?

A **class method** is a method that is bound to the class, not the instance. It receives the class itself as the first argument, typically named `cls`.

### Key Characteristics

* **Decorator:** Uses `@classmethod`.
* **Argument:** Receives `cls` instead of `self`.
* **Use Case:** Often used as **factory methods**—alternatives to `__init__` that create class instances with different sets of parameters.

```python
class Date:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date_str):
        day, month, year = map(int, date_str.split('-'))
        return cls(day, month, year) # Creates an instance using the class

```

## What is a Static Method?

A **static method** is a method that behaves like a regular function but lives inside a class namespace. It does not receive any implicit first argument (no `self`, no `cls`).

### Key Characteristics

* **Decorator:** Uses `@staticmethod`.
* **Argument:** No implicit first argument.
* **Use Case:** Used when a function logically belongs to a class but doesn't need to access any properties or methods of the class or instance. It is essentially a "utility" function.

```python
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

```

## Comparison Summary

| Feature | Instance Method | Class Method | Static Method |
| --- | --- | --- | --- |
| **Decorator** | None | `@classmethod` | `@staticmethod` |
| **First Argument** | `self` (instance) | `cls` (class) | None |
| **Access** | Can modify instance/class | Can modify class | None |
| **Primary Use** | Instance logic | Factory methods | Utility functions |

## Which one should you choose?

1. **Use `classmethod**` when you need to access or modify the class state, or when you need an alternative constructor.
2. **Use `staticmethod**` when the logic is related to the class but doesn't require access to the class or instance state (e.g., validation logic, formatting utilities).
3. **Use `instancemethod**` by default when you need to interact with the specific object instance.

{% raw %}

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

{% endraw %}

