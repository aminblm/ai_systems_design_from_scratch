---

title: "The Resilience Boundary: Try-Except vs. Raising Errors"
description: "Learn the essential distinction between handling errors locally and bubbling them up in your application architecture."
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



# The Resilience Boundary: Handling vs. Bubbling

{% raw %}

<div class="author-card">
    <p><strong>{{ site.author.name }}</strong> — <i>{{ site.author.bio }}</i></p>
</div>

{% endraw %}


A common point of confusion in Python development is deciding where to catch an error and where to let it propagate. Understanding this "resilience boundary" is key to writing clean, maintainable systems.

## The Rule of Responsibility

The decision between `try-except` (handling) and `raise` (bubbling) rests on one fundamental question: **"Can this specific layer do something meaningful to recover?"**

## When to Use `try-except` (Handle)

Use `try-except` only when you can resolve the issue, provide a fallback, or perform essential cleanup before moving on. 

* **You can provide a default**: If a network request fails, can you load a cached version of the data?
* **You must cleanup**: Even if you can't fix the error, you must release a file lock or close a socket (RAII).
* **You are at the top level**: Your main application loop should catch errors to log them and prevent the entire system from crashing.

```python
try:
    data = fetch_config()
except NetworkError:
    # We can recover by using a local default
    data = load_default_config() 

```

## When to Use `raise` (Bubble)

Raise an error (or let it propagate) when you cannot fix the underlying issue. Bubbling errors up is not a failure; it is a way to ensure that the error is handled by a component with enough context to make a correct decision.

* **Missing Context**: A low-level `Git` module shouldn't decide how to display a GUI error message to a user. It should raise the exception.
* **Preventing "Silent Failures"**: If you catch an error but do nothing (e.g., `pass`), you are burying critical bugs.
* **API Integrity**: If your function is passed invalid input, `raise ValueError` immediately. It is better to fail loud and fast than to continue with corrupt state.

```python
def process_git_push(repo):
    if not repo.is_clean():
        # We cannot recover here; bubble up to the caller
        raise GitError("Cannot push: Repo not clean.")

```

## The "Translate" Pattern

Sometimes, you need to catch a low-level exception and re-raise a more descriptive, high-level exception. This preserves the error context while hiding internal implementation details.

```python
try:
    db.execute_query()
except SqliteError as e:
    # Translate low-level DB errors to domain-specific errors
    raise DatabaseAccessError("Failed to update user profile") from e

```

## Best Practices

| Strategy | When to Apply |
| --- | --- |
| **Handle** | When you have a viable fallback or cleanup task. |
| **Bubble** | When the caller has more context to resolve the issue. |
| **Translate** | When internal errors need to be mapped to public API errors. |

* **Never Use Bare `except**`: Always catch specific exceptions (e.g., `except ConnectionError:`). Bare `except:` clauses hide bugs.
* **Fail Loudly**: If you don't know exactly how to recover, let the exception bubble up. It is easier to debug an unhandled exception than one that was silently swallowed.

By being intentional about where you handle errors, you stop writing code that hides problems and start writing code that reports them precisely where they occur.

{% raw %}
---

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

{% endraw %}

