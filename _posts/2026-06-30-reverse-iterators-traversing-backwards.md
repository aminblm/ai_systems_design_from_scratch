---

title: "Mastering Reverse Iterators in Python"
description: "How to efficiently traverse sequences in reverse using built-in Python tools."
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


# Reverse Iterators: Traversing Backwards

{% raw %}

<div class="author-card">
    <p><strong>Amin Boulouma</strong>, <i>Software Engineer</i></p>
</div>

{% endraw %}



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

{% raw %}

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

{% endraw %}

