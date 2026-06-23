---

title: "Building a Robust SEO Slug Compiler"
description: "Learn how to transform raw user input into web-safe, standardized Jekyll post filenames using normalization and character-set sanitization."
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



# SEO Slug Compilers: Standardizing Filenames

{% raw %}

<div class="author-card">
    <p><strong>{{ site.author.name }}</strong> — <i>{{ site.author.bio }}</i></p>
</div>

{% endraw %}


For static site generators like Jekyll, the post filename is not just metadata—it is the URL structure. A proper filename must adhere to strict rules: no special characters, no spaces, and standardized date-prefixing. The `ResilientSlugGenerator` and `JekyllFilenameController` classes demonstrate a professional-grade pipeline for this task.

## The Normalization Pipeline

The conversion process is a multi-stage "purification" pipeline. Every step ensures the output becomes increasingly compliant with web URL standards.



1.  **Unicode Decomposition (NFKD)**: This is the most crucial step. It breaks down complex characters (like `é`) into their base characters (`e`) and combining accents, allowing them to be stripped during the ASCII conversion phase.
2.  **ASCII Sanitization**: Stripping non-ASCII characters ensures your URLs work across all browsers and server environments without encoding issues.
3.  **Regex Purging**: We use `re.sub(r'[^\w\s-]', '', text)` to remove any character that is not a word character (letters, numbers, underscores), a space, or a hyphen.
4.  **Token Normalization**: Finally, we collapse multiple spaces or hyphens into a single hyphen delimiter (`-`), resulting in clean tokens like `this-is-my-post`.

## Architectural Workflow: Jekyll Controller

The `JekyllFilenameController` encapsulates this logic and adds filesystem context—specifically, the **date-prefix requirement** (e.g., `YYYY-MM-DD-slug.md`).

* **Dynamic Date Computation**: By using a property `current_date_string` rather than a static variable in `__init__`, the compiler avoids "date drift." If the application runs across midnight, it will accurately pick up the new date without requiring a restart.
* **CLI Interaction Loop**: The `start_generator_interface` manages the user's terminal experience, providing an "infinite polling" mode that handles signals like `Ctrl+C` (KeyboardInterrupt) gracefully, ensuring no terminal state corruption occurs upon exit.

### The Slug Transformation Core
```python
def transform_to_slug(self, text: str) -> str:
    # 1. Normalize unicode to standard ASCII
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    # 2. Lowercase and strip invalid characters
    text = re.sub(r'[^\w\s-]', '', text.lower()).strip()
    # 3. Collapse whitespace to single hyphens
    return re.sub(r'[-\s]+', '-', text).strip('-')

```

## Best Practices

* **Fail Fast**: If the input is empty or contains no alphanumeric characters, the engine informs the user immediately rather than generating a broken filename like `2026-06-23-.md`.
* **Idempotency**: The engine takes the same input and produces the same output every time, ensuring that even if you re-run the compiler, your file naming remains consistent.
* **Separation of Concerns**: The `ResilientSlugGenerator` is pure logic—it doesn't know about files, dates, or Jekyll. The `JekyllFilenameController` handles the "business logic" of how that slug fits into your project folder. This makes the generator highly reusable in other parts of your system.

By decomposing your slug generation into these modular steps, you create a system that is easily testable, highly predictable, and perfectly suited for automation.

{% raw %}


<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

{% endraw %}

