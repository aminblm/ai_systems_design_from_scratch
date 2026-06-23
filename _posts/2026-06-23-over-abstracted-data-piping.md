---

title: "The Trap of Over-Abstraction: When Less Is More"
description: "Learn why adding unnecessary layers of abstraction can hurt code readability and how to simplify your data pipelines for better maintainability."
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


<div style="text-align: center; margin: 2rem 0; padding-bottom: 1rem; border-bottom: 1px solid #e9ebec;">
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">🏠 Documentation Hub</a>
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/blog" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">📝 Engineering Blog</a>
  <a href="https://github.com/aminblm/ai_systems_design_from_scratch" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">💻 GitHub Repository</a>
</div>



# Over-abstracted Data Piping


<div class="author-card">
    <p><strong>{{ site.author.name }}</strong> — <i>{{ site.author.bio }}</i></p>
</div>


In software engineering, we are taught to avoid duplication and abstract logic into managers. However, there is a point where abstraction becomes a liability. A classic example is the `DependenciesManager` class that exists solely to return a 4-tuple, which is then immediately unpacked into a target function. 

This is **over-abstraction**: it adds a layer of indirection that provides zero functional value while significantly increasing the cognitive load for anyone reading your code.

## The Problem: Obscured Data Flow

When a class is nothing more than a wrapper for a data structure (the 4-tuple), it creates a "hidden" dependency. The reader must jump between files to see what the `DependenciesManager` returns, only to find that it was just a simple grouping of variables that could have been handled explicitly.



### The Over-Abstracted Pattern
```python
# Unnecessary complexity
class DependenciesManager:
    def get_deps(self):
        return (config, db, logger, cache)

# In the main flow:
# The reader has to trace back to DependenciesManager to know what these 4 items are.
config, db, logger, cache = manager.get_deps()
Jekyll.generate_site(*args) 

```

## The Solution: Explicit Data Handling

If your "manager" isn't managing state or logic, **delete it**. Replacing the over-abstraction with explicit variable initialization or a simple `dataclass` makes your code self-documenting and immediately readable.

### The Simplified Approach

```python
from dataclasses import dataclass

@dataclass
class SiteDependencies:
    config: Config
    db: Database
    logger: Logger
    cache: Cache

# Now the flow is explicit:
deps = SiteDependencies(config, db, logger, cache)
Jekyll.generate_site(deps)

```

## Why Simplicity Wins

1. **Reduced Cognitive Load**: When you look at the `SiteDependencies` dataclass, you know exactly what data is being passed without needing to jump to a "Manager" class.
2. **Type Safety**: By using a `dataclass` or a `NamedTuple`, you get IDE autocompletion and static type checking that a generic tuple unpacking (`*`) completely hides.
3. **Readability**: The code now documents its own intent. You aren't "piping" data; you are passing a well-defined object.

## Best Practices for Evaluating Abstractions

* **The "Three-Use" Rule**: Don't create an abstraction unless you are certain it will be used in at least three distinct places. If it's only used once, it's just clutter.
* **Beware of "Manager" Suffixes**: Classes named `SomethingManager` or `SomethingHandler` are often signs of over-abstraction. Ask yourself: is this class *managing* anything, or is it just acting as a pass-through?
* **Prefer Explicit over Implicit**: If you find yourself using the `*` (unpacking) operator frequently to pipe data between classes, consider if you are hiding the structure of your data from the next developer.

By stripping away the unnecessary wrappers, you make your codebase more approachable and easier to debug. Sometimes, the best code is the code you decide not to write.

---

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

