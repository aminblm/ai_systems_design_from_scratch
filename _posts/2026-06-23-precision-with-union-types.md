---


title: "Type Safety: Mastering Union Types in Python"
description: "Learn how to use Union types to improve code clarity and type safety when functions accept multiple data types."
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



# Precision with Union Types

<div class="author-card">
    <p><strong>{{ site.author.name }}</strong> — <i>{{ site.author.bio }}</i></p>
</div>


As Python’s type hinting system has matured, `Union` types have become an essential tool for expressing that a function or variable can hold one of several different types. By using `Union`, you move away from the ambiguity of "it could be anything" and toward a self-documenting, statically verifiable codebase.

## The Problem: The Ambiguity of `Any`

When a function accepts a parameter that could be either an `int` or a `str`, the lazy approach is to use `Any` or no type hint at all. This forces the reader (and static analysis tools like `mypy`) to guess what the code expects, leading to runtime errors that could have been caught during development.

## The Solution: Using `Union`

A `Union` type explicitly defines the set of allowed types. If a value does not match one of these types, your IDE and type checker will flag it immediately.

### Implementation
```python
from typing import Union

def process_id(identifier: Union[int, str]) -> str:
    # Python 3.10+ also supports the pipe syntax: int | str
    return f"Processing ID: {str(identifier)}"

# These are valid
process_id(123)
process_id("abc-456")

# This would trigger a type-checker error
# process_id(None)

```

## Modern Syntax: The Pipe Operator (`|`)

In Python 3.10 and newer, the `Union` import is largely optional. You can use the more concise pipe operator (`|`), which is visually clearer and follows standard set notation.

```python
# The modern, cleaner way
def format_input(data: int | str | list[int]) -> str:
    ...

```

## When to Use Union Types

1. **Flexible APIs**: Use `Union` when a function is designed to handle multiple common input types, like an ID that can be a numeric index or a unique string slug.
2. **Optional Values**: While `Optional[T]` is the standard for "T or None", `Union[T, None]` is technically identical. Use `| None` for modern, readable code.
3. **Result Normalization**: When a function can return different "shapes" of data (e.g., a `Success` object or an `Error` object), `Union` helps the caller handle those cases explicitly.

## Best Practices

* **Exhaustive Matching**: When you return a `Union`, pair it with `match-case` (the structural pattern matching we discussed earlier). This allows you to write code that is guaranteed to handle all possible types defined in your `Union`.
* **Keep Unions Small**: If your `Union` contains more than three or four types, it might be a sign that your function is doing too much. Consider whether you should introduce a common base class or interface instead.
* **Prioritize `|` (Pipe)**: If your project supports Python 3.10+, prefer the pipe operator over `Union[...]`. It is easier to read and requires less boilerplate.

By being explicit about the types your code handles, you shift the burden of validation from your runtime logic to your development environment. This leads to fewer bugs and a much better developer experience.

{% raw %}


<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

{% endraw %}

