---

title: "The Danger of Implicit Dependency Injection"
description: "Why relying on kwargs in decorators leads to brittle APIs and silent bypasses of critical validation logic."
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



# Hidden Inputs and Side-Effecting Decorators


<div class="author-card">
    <p><strong>{{ site.author.name }}</strong> — <i>{{ site.author.bio }}</i></p>
</div>


Decorators are powerful tools for cross-cutting concerns, but they become a liability when they depend on *how* a function is called rather than *what* a function is. Relying on `kwargs` for validation—like looking for `input_dir` inside a decorator—creates an API where the slightest deviation in calling syntax causes security and logic failures.

## The Problem: Positional vs. Keyword Fragility

If your decorator looks for `'input_dir'` in `kwargs`, it assumes the developer will always use keyword arguments. However, Python allows positional arguments, which are invisible to `kwargs`.



### The Fragile Pattern
```python
def with_error_handling(func):
    def wrapper(*args, **kwargs):
        # Fragile: This logic is bypassed if input_dir is passed positionally!
        input_dir = kwargs.get('input_dir') 
        if not input_dir:
            raise ValueError("Input directory required")
        return func(*args, **kwargs)
    return wrapper

```

If a developer calls `generate_html_pages("/data/in")`, `kwargs` is empty, your validation logic is skipped, and your application potentially operates on unvalidated or null input.

## The Solution: Normalizing the Signature

To build decorators that are robust against different calling styles, you must synchronize the input arguments with the function signature using `inspect.signature`.

### The Robust Pattern

```python
import inspect
from functools import wraps

def with_error_handling(func):
    sig = inspect.signature(func)
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Bind positional and keyword arguments to the function signature
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        input_dir = bound_args.arguments.get('input_dir')
        if not input_dir:
            raise ValueError("Input directory required")
            
        return func(*args, **kwargs)
    return wrapper

```

## Why Signature Binding Wins

1. **Uniformity**: It treats `generate_html_pages(input_dir="/data")` and `generate_html_pages("/data")` as identical, ensuring your validation logic is **always** executed.
2. **Explicit Contracts**: By using `inspect`, you acknowledge that your decorator has a dependency on the function signature, making the code self-documenting.
3. **Future-Proofing**: If you add more required arguments to your functions, the `bind()` logic handles them automatically without requiring manual `kwargs` updates in every decorator.

## Comparison of Argument Handling

| Strategy | Validation Reliability | API Flexibility | Code Complexity |
| --- | --- | --- | --- |
| **`kwargs.get()`** | Extremely Low (Fragile) | Poor | Low |
| **Explicit `args[0]**` | Moderate (Index-dependent) | Rigid | Moderate |
| **`inspect.signature`** | **High (Robust)** | **High** | **Moderate** |

## Best Practices

* **Avoid Implicit Dependencies**: If a decorator needs an argument, try to make it an argument *of the decorator* (e.g., `@validate(arg='input_dir')`) rather than searching for it inside the function's runtime inputs.
* **Use `functools.wraps**`: Always use `@wraps(func)` to ensure your decorated function retains its original metadata, docstrings, and signature.
* **Fail Loudly**: If your decorator detects that a required argument is missing, raise a `TypeError` or `ValueError` immediately rather than attempting to proceed with `None`.

By shifting from "guessing" the input through dictionary lookups to "binding" it via signature inspection, you eliminate one of the most common and dangerous failure modes in Python's decorator ecosystem.

---

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

