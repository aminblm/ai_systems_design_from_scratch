---

title: "Designing Request-Handler Layouts in Python"
description: "How to structure flexible URL routing patterns for your Python web applications."
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



# Designing Request-Handler Layouts


<div class="author-card">
    <p><strong>{{ site.author.name }}</strong> — <i>{{ site.author.bio }}</i></p>
</div>


In Python web development, mapping incoming HTTP requests to specific logic is the backbone of any framework. Using a dictionary-based routing table—specifically structured as `self._routes[HTTP_METHOD][URL_PATH] = Handler_Callback`—is a highly efficient and performant way to manage application traffic.

## The Routing Architecture

This layout treats your application state as a nested map. This structure allows for $O(1)$ constant-time lookup complexity when dispatching requests.



### Implementation Example

By organizing routes this way, you decouple the routing logic from the business logic, allowing your handlers to remain clean and focused.

```python
class Router:
    def __init__(self):
        # Structure: { METHOD: { PATH: CALLBACK } }
        self._routes = {
            "GET": {},
            "POST": {},
        }

    def add_route(self, method, path, callback):
        self._routes[method.upper()][path] = callback

    def dispatch(self, method, path):
        # O(1) lookup
        handler = self._routes.get(method.upper(), {}).get(path)
        if handler:
            return handler()
        return "404 Not Found"

# Usage
router = Router()
router.add_route("GET", "/index", lambda: "Hello World")

print(router.dispatch("GET", "/index"))

```

---

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

