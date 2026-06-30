---

title: "Managed Polymorphism: Using 'Any' and Class Names"
description: "Exploring strategies for handling dynamic types in Python using type hints and runtime class inspection."
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

# Managed Polymorphism: Type Flexibility

{% raw %}
<div class="author-card">
    <p><strong>Amin Boulouma</strong>, <i>Software Engineer</i></p>
</div>
{% endraw %}


Polymorphism allows your code to treat different objects as instances of a general interface. In dynamic languages like Python, we often manage this using `typing.Any` or by inspecting the object's class name at runtime. 

## The Challenge: Type Safety vs. Flexibility
When a function accepts "anything," you lose the benefits of static analysis. "Managed" polymorphism is about retaining control—ensuring that even if you accept `Any` type, your logic safely identifies and handles the specific child class before proceeding.



## Pattern 1: Runtime Inspection
Instead of relying solely on duck-typing, you can use the object's class name or `isinstance` checks to branch your logic. This is common when your `SocketServer` needs to handle different command types differently.

```python
from typing import Any

def handle_request(obj: Any) -> None:
    # Use __class__.__name__ to manage polymorphic behavior
    class_name = obj.__class__.__name__
    
    if class_name == "LoginRequest":
        _handle_login(obj)
    elif class_name == "DataRequest":
        _handle_data(obj)
    else:
        raise ValueError(f"Unsupported polymorphic type: {class_name}")

```

## Pattern 2: The `Any` Type Hint

Using `Any` is a signal that you are bypassing strict type checking. To "manage" this, use it in conjunction with **Type Guards** or **Factory Patterns**.

## Best Practices for Managed Polymorphism

1. **Prefer `isinstance()` over `__class__.__name__`:** Checking the name of the class is brittle (it breaks if you rename the class). `isinstance(obj, BaseClass)` is more robust and idiomatic Python.
2. **Exhaustive Handling:** If you are using polymorphism to switch between types, ensure you have an `else` clause that logs or raises an error for unexpected types.
3. **Use Protocol (Structural Typing):** If you find yourself checking `__class__.__name__` frequently, you are likely missing a shared interface. Define a `Protocol` to describe what methods these polymorphic objects should have.

```python
from typing import Protocol

class Request(Protocol):
    def process(self) -> None:
        ...

# Now your server handles any object that satisfies the 'Request' protocol
def execute(req: Request) -> None:
    req.process()

```

## Summary Checklist

* **Identify:** Are you using `Any` because you genuinely don't know the type, or because you haven't defined a shared interface?
* **Validate:** Use `isinstance()` or `Protocol` to enforce behavior, rather than relying on brittle string comparisons of class names.
* **Document:** If you must use `Any`, clearly comment on the expected interface of the polymorphic objects.

{% raw %}
<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>
{% endraw %}
