---

title: "Composition over Abstraction: Why Pipelines Win"
description: "Exploring the power of function composition through Python's functional programming patterns."
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

# Composition over Abstraction

{% raw %}
<div class="author-card">
    <p><strong>Amin Boulouma</strong>, <i>Software Engineer</i></p>
</div>
{% endraw %}


The code snippet `IOUtility.text_to_lines_generator(IOUtility.read_decoded(file_path))` is a classic example of **function composition**. Instead of creating a complex "God Object" or a deeply nested class hierarchy (over-abstraction), you are piping data through small, focused, and reusable functions.

## The Concept: Composition vs. Abstraction

* **Abstraction** often involves hiding complexity behind interfaces or classes, which can lead to "abstraction bloat"—where you spend more time managing the structure than the data.
* **Composition** is the act of combining simple, distinct functions to create more complex logic. By passing the output of one function directly into the input of another, you keep your logic modular and testable.



## Analyzing Your Pattern

Your snippet is a perfect example of a **data pipeline**. 

```python
# The Nested Approach (Harder to read as it grows)
result = IOUtility.text_to_lines_generator(IOUtility.read_decoded(file_path))

# The Composed Approach (More readable for complex pipelines)
raw_data = IOUtility.read_decoded(file_path)
lines = IOUtility.text_to_lines_generator(raw_data)

```

### Why this is superior to heavy abstraction:

1. **Loose Coupling:** Each function is agnostic of the other. `text_to_lines_generator` doesn't care *where* the text came from, only that it is a string.
2. **Testability:** You can unit test `read_decoded` and `text_to_lines_generator` in isolation.
3. **Flexibility:** If you want to change how you read files (e.g., adding encryption), you only change the first function in the chain, not the entire pipeline architecture.

## Visualizing the Pipeline

In a composition-heavy architecture, you view your system as a series of transformations:

## When to prioritize Composition

* **Data Processing:** Any task involving ETL (Extract, Transform, Load) or streams.
* **Middleware:** Request/Response cycles in web frameworks.
* **Utility Libraries:** When functions don't need to hold "state."

By avoiding excessive abstraction—such as creating an `FileProcessor` class that holds internal state—and favoring functional composition, you ensure your code remains agile and easy to debug.

{% raw %}
<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>
{% endraw %}
