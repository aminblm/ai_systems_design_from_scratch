---

title: "Mastering Multiple Inheritance and MRO in Python"
description: "A guide to understanding how Python resolves method calls in complex inheritance hierarchies using the C3 linearization algorithm."
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


# Multiple Inheritance: Navigating the Hierarchy

{% raw %}

<div class="author-card">
    <p><strong>Amin Boulouma</strong>, <i>Software Engineer</i></p>
</div>

{% endraw %}



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

{% raw %}

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

{% endraw %}

