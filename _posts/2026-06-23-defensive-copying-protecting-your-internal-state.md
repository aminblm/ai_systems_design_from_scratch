---


title: "The Importance of Defensive Copying in Python"
description: "Learn how to prevent side-effect bugs by returning copies of mutable collections rather than the original references."
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



# Defensive Copying: Protecting Your Internal State

<div class="author-card">
    <p><strong>Amin Boulouma</strong> — <i>Software Engineer</i></p>
</div>


In Python, collections like `list`, `dict`, and `set` are mutable objects. When you store these in a class and expose them via a getter method, returning the original reference is a common source of "spooky action at a distance"—where external code accidentally modifies your internal state.

## The Problem: The "Reference Leak"

If your class returns the original reference to its internal list, any external caller can mutate that list, causing your object's internal state to change without its knowledge.

### The Leaky Pattern:
```python
class DocumentManager:
    def __init__(self):
        self._documents = ["doc1.txt", "doc2.txt"]

    def get_documents(self):
        # DANGER: Returning a reference to the internal list
        return self._documents

# External code
manager = DocumentManager()
docs = manager.get_documents()
docs.append("malicious_doc.txt") # Modifies the internal state of 'manager'!

```

## The Solution: Return a Copy

By returning `self.documents.copy()`, you return a shallow copy of the collection. The external caller now has its own version of the data, and any modifications it makes will not affect your class's private state.

### The Robust Pattern:

```python
class DocumentManager:
    def __init__(self):
        self._documents = ["doc1.txt", "doc2.txt"]

    def get_documents(self):
        # SAFE: Returning a shallow copy
        return self._documents.copy()

# External code
manager = DocumentManager()
docs = manager.get_documents()
docs.append("safe_doc.txt") # manager._documents remains unchanged!

```

## When to Copy vs. When to Encapsulate

* **Shallow vs. Deep Copies**: `.copy()` (or list slicing `[:]`) creates a shallow copy. If your list contains other mutable objects (like nested lists), those nested objects are still references! If you need to protect nested data, use `copy.deepcopy()`.
* **Encapsulation**: Alternatively, instead of returning the collection, expose methods that act on the collection (e.g., `manager.add_document()`, `manager.get_document_count()`). This is often the cleanest architectural choice.
* **Tuples**: If the collection should never be modified, consider converting it to a `tuple` before returning it. Tuples are immutable and provide a "read-only" guarantee that a list copy cannot.

## Best Practices

* **Default to Immutability**: If a getter is meant to be read-only, ensure the caller cannot modify the original data.
* **Performance Note**: For very large collections, copying every time `get_documents()` is called can have a performance cost. If performance is critical, return a `tuple` or an iterator instead.
* **Be Intentional**: Always ask yourself: *Should the consumer be allowed to modify this state?* If the answer is no, protect it with a copy or an immutable wrapper.

Defensive copying is a simple technique that prevents subtle, hard-to-track bugs. By keeping your class's internal state encapsulated, you create a system that is predictable, robust, and much easier to debug.

{% raw %}


<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

{% endraw %}

