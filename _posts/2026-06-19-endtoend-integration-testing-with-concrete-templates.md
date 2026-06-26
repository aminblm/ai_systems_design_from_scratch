---
layout: default
title: "End-to-End Integration Testing of Jekyll with Concrete Templates"
description: "Putting it all together: Validating the static site pipeline with recursive variable hydration, master layouts, and real compilation streams."
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

<div style="text-align: center; margin: 2rem 0; padding-bottom: 1rem; border-bottom: 1px solid #e9ebec;">
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">🏠 Documentation Hub</a>
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/blog" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">📝 Engineering Blog</a>
  <a href="https://github.com/aminblm/ai_systems_design_from_scratch" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">💻 GitHub Repository</a>
</div>


# End-to-End Integration Testing of Jekyll with Concrete Templates

<div class="author-card">
    <p><strong>Amin Boulouma</strong>,  <i>Software Engineer</i></p>
</div>

We have constructed individual parsing processors for Markdown and YAML, implemented clean abstraction wrappers around network/file I/O operations, and engineered an orchestration facade. To tie our series together, let's look at an **end-to-end integration test case** using a concrete layout schema and global configuration payload.

This walkthrough demonstrates exactly how our token hydration system marries templates, asset definitions, and static configurations together in production.

---

## 1. The Inputs: Configuration and Base Layout

To initialize the compilation pipeline, the site relies on two vital core files: a localized global state configuration (`config.yaml`) and an HTML template blueprint shell (`layout.html`).

### Global Site State (`config.yaml`)

This configuration models key-value data mappings containing site-wide attributes:

```yaml
title: AI Systems Design From First Principles
description: Rebuilding enterprise systems and AI from first principles.
url: https://aminblm.github.io/ai_systems_design_from_scratch
css: ../styles.css
author: Amin Boulouma
footer_text: AI Systems Design From First Principles

```

### The Document Blueprint (`layout.html`)

This file uses explicit Liquid-style double-curly-brace interpolation markers (`{{ site.<key> }}`) to indicate exactly where dynamic content strings belong:

```html
<!DOCTYPE html>
<html>
    <head>
        <title> {{ site.title }} </title>
        <link rel="stylesheet" href="{{ site.css }}">
    </head>
    <body>
        <div class="hero">
            <header>
                <h1>{{ site.title }}</h1>
                <p>{{ site.description }}</p>
            </header>
        </div>
        
        <main>
            <div class="container">
                {{ site.content }}
            </div>
        </main>

        <footer>
            <div class="container">
                <p><a href="{{ site.url }}">{{ site.footer_text }} by {{ site.author }}</a></p>
            </div>
        </footer>
    </body>
</html>

```

---

## 2. Behind the Scenes: The Hydration Logic

When you trigger the entrypoint via `Jekyll.generate_site(input_dir, layout_path, config_file_path)`, our engine handles compilation through an elegant substitution loop inside `HTMLRenderer.render_html`.

Let's look at the data mutation sequence step-by-step:

### Step A: Markdown Splitting & Translation

First, the rendering framework isolates an active post (e.g., `welcome.md`) and compiles its markdown payload to raw structural HTML. The template placeholder is then swapped out with this newly generated content body:

```python
html = layout.replace('{{ site.content }}', MarkdownToHTMLBuilder.create_from_file(md_file_path).md_file_to_html())

```

### Step B: Recursive Dictionary Hydration

Next, our `YAMLParser` mapping object is looped over line by line. Every key found inside `config.yaml` explicitly overwrites its matching layout placeholder:

```python
for key in config: 
    html = html.replace('{{ site.' + key + ' }}', config[key])

```

---

## 3. The Compiled Output

Once `FileOperations.write_html_content` finishes committing the text stream to disk inside the newly formed `/output` destination folder, your resulting output is a completely unified, zero-dependency HTML document ready for delivery:

```html
<!DOCTYPE html>
<html>
    <head>
        <title> AI Systems Design From First Principles </title>
        <link rel="stylesheet" href="../styles.css">
    </head>
    <body>
        <div class="hero">
            <header>
                <h1>AI Systems Design From First Principles</h1>
                <p>Rebuilding enterprise systems and AI from first principles.</p>
            </header>
        </div>
        
        <main>
            <div class="container">
                <p>Welcome to the first principles system generation workspace!</p>
            </div>
        </main>

        <footer>
            <div class="container">
                <p><a href="https://aminblm.github.io/ai_systems_design_from_scratch">AI Systems Design From First Principles by Amin Boulouma</a></p>
            </div>
        </footer>
    </body>
</html>

```

---

## Systems Review and Architecture Summary

Over this multi-part series, we took a seemingly complex task, cloning an enterprise static site generator, and split it into lightweight, single-responsibility layers:

* **`Jekyll` Facade:** Provides a clean single-line API for compilation.
* **`DependenciesManager`:** Decouples file lookups and loading from the transformation logic.
* **`HTMLRenderer`:** Handles string template compilation as a deterministic, stateless pipe.
* **`ErrorHandler`:** Abstracts out error boundaries via clean Python decorators, protecting processing loops from runtime edge-case crashes.

By designing code around explicit boundaries and relying on zero external packages, your architecture remains fast, stable, and simple to test or extend indefinitely.

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>