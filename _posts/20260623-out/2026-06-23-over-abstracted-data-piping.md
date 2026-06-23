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

---

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

