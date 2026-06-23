---

title: "Structural Modeling: Trees and Dataclasses"
description: "Learn how to represent hierarchical system architectures using recursive dataclass structures and HTML rendering."
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



# Structural Modeling: Representing Hierarchies


<div class="author-card">
    <p><strong>{{ site.author.name }}</strong> — <i>{{ site.author.bio }}</i></p>
</div>


When modeling complex systems—like microservice topologies or infrastructure maps—we often need a way to represent parent-child relationships. The `dataclass` pattern combined with a recursive rendering structure is the most Pythonic and efficient way to map these hierarchical models to visual representations like HTML or graphs.

## The Power of Recursive Dataclasses

A recursive `dataclass` allows you to define a node that can contain an arbitrary number of nested sub-nodes. This structure mirrors the way physical and logical architectures are organized.



### Key Components
* **`ArchComponent`**: Uses `field(default_factory=list)` to initialize an empty list for children, avoiding the common "mutable default argument" pitfall in Python.
* **`ArchitectureRenderer`**: By separating the *data structure* (`ArchComponent`) from the *visualization logic* (`ArchitectureRenderer`), you adhere to the **Single Responsibility Principle**.

## Implementation Detail: Recursive Rendering

The `_render_node` method is the core of the hierarchy. It doesn't need to know the depth of the architecture; it simply renders the current node and asks its children to render themselves.

```python
    def _render_node(self, node: ArchComponent) -> str:
        # Recursively call _render_node for every child
        child_html = "".join([self._render_node(c) for c in node.children])
        return f"""
        <div class="component type-{node.component_type}">
            <span class="label">{node.name}</span>
            {child_html}
        </div>
        """

```

## Why This Approach Works

1. **Infinite Scalability**: This pattern works for a 2-level hierarchy or a 20-level hierarchy without changing a single line of code.
2. **Visual Semantics**: By mapping `component_type` to CSS classes (e.g., `type-service`), you can instantly change the look and feel of the entire architecture just by editing the CSS string.
3. **Type Safety**: Dataclasses provide a clear, typed contract for what a component is, making the code much easier to refactor than a loose dictionary-based tree.

## Best Practices

* **Decouple CSS**: While the CSS is inline for simplicity here, in production, move it to a dedicated `.css` file or a template system like Jinja2.
* **Validation**: Add a `__post_init__` method to your `ArchComponent` to ensure that `component_type` matches a predefined list of allowed infrastructure types.
* **Cycle Detection**: If your architecture graphs could potentially have circular references (e.g., Service A depends on Service B, which depends on Service A), add a "visited" set to your renderer to prevent an infinite recursion crash.

By leveraging recursive structures, you turn the complex task of rendering nested architectures into a predictable, automated process. You are no longer managing nodes; you are managing the *logic* that flows through them.

---

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

