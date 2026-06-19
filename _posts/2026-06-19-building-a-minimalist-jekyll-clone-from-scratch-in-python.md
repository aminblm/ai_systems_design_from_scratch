---
layout: default
title: "Building a Minimalist Jekyll Clone From Scratch in Python"
description: "Demystifying static site generators: Implementing a zero-dependency Jekyll clone in Python using the Facade pattern and a decoupled architecture."
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

# Building a Minimalist Jekyll Clone From Scratch in Python

<div class="author-card">
    <p><strong>{{ site.author.name }}</strong> — <i>{{ site.author.bio }}</i></p>
</div>

Have you ever wondered how static site generators like Jekyll actually work under the hood? They feel like magic: you throw in some Markdown files, a YAML configuration, and an HTML layout, and boom—out pops a fully rendered website.

Instead of relying on heavy third-party frameworks, we can build our own minimalist Jekyll clone using native architectural patterns and a custom, local toolchain. Here is a breakdown of how to build a static site engine using clean code principles and Python.

---

## The Architecture: Micro-Libraries & Separation of Concerns

A great software design rule is to separate the *parsing engines* from the *orchestration engine*. In this implementation, the actual parsing of formats is handled by abstract local utilities built entirely from scratch:

* `YAMLBuilder`: Parses configuration files into usable dictionary mappings.
* `MarkdownToHTMLBuilder`: The core engine converting `.md` content to structural HTML.
* `FileOperationsUtility`: Handles low-level, encoded IO operations safely.

By treating these as isolated dependencies, our main orchestrator (`Jekyll`) only has to worry about structural workflow logic rather than individual file-parsing regex.

---

## Design Patterns in Play

To keep the application modular, predictable, and highly testable, the codebase leverages several classic software design patterns:

### 1. The Facade Pattern (`Jekyll`)

The `Jekyll` class serves as a clean, simple interface to a complex subsystem. Instead of making the user coordinate directory reading, dependency gathering, HTML rendering, and writing, they simply call a single unified endpoint:

```python
Jekyll.generate_site(input_dir, layout_path, config_file_path)

```

### 2. The Decorator Pattern (`ErrorHandler`)

Error handling can quickly clutter business logic. By leveraging Python decorators, the codebase abstracts error boundaries out of the generation loop. The `@ErrorHandler.with_error_handling` wrapper guarantees that file or processing failures are cleanly caught, logged with tracebacks, and managed without crashing the entire build pipeline.

### 3. The Builder / Factory Interface

Instead of parsing raw strings dynamically throughout the lifecycle, dependencies are instantiated via semantic builder interfaces like `YAMLBuilder.create_from_file()` and `MarkdownToHTMLBuilder.create_from_file()`. This keeps object creation isolated and consistent.

---

## Core Code Walkthrough

Here is the lightweight, structural pipeline implemented to manage the site assembly:

```python
import os
import logging
import traceback

from ai_systems_design.py_yaml import YAMLBuilder
from ai_systems_design.py_markdown_to_html.py_markdown_to_html import MarkdownToHTMLBuilder
from ai_systems_design.utils import FileOperationsUtility

class ErrorHandler:
    @staticmethod
    def with_error_handling(func):
        def wrapper(*args, **kwargs):
            if 'input_dir' in kwargs and not os.path.isdir(kwargs['input_dir']):
                raise ValueError(f"Input dir {kwargs['input_dir']} is not a dir.")
            try: 
                return func(*args, **kwargs)
            except Exception as e: 
                logging.error(f"Error in {func.__name__}: {e}") 
                logging.error(traceback.format_exc())
                return None
        return wrapper

class FileOperations:
    @staticmethod
    def get_file_paths(md_file_name, input_dir, output_dir):
        html_file_name = f"{md_file_name.split('.md')[0]}.html"
        return tuple(map(lambda x, y: os.path.join(x, y), (input_dir, output_dir), (md_file_name, html_file_name)))
  
    @staticmethod
    @ErrorHandler.with_error_handling
    def create_output_dir(input_dir):
        output_dir = os.path.join(os.path.dirname(input_dir), 'output')
        if not os.path.exists(output_dir): 
            os.makedirs(output_dir, exist_ok=True)
        return output_dir
    
    @staticmethod
    def write_html_content(md_file_path, html_file_path, layout, config):
        FileOperationsUtility.write_encoded(html_file_path, HTMLRenderer.render_html(layout, config, md_file_path))

    @staticmethod 
    def read_html_file(html_file_path): 
        return FileOperationsUtility.read_decoded(html_file_path)

class HTMLRenderer:
    @staticmethod
    def render_html(layout, config, md_file_path):
        # Convert markdown and inject into layout template
        markdown_html = MarkdownToHTMLBuilder.create_from_file(md_file_path).md_file_to_html()
        html = layout.replace('{{ site.content }}', markdown_html)
        
        # Hydrate dynamic configuration variables
        for key in config: 
            html = html.replace('{{ site.' + key + ' }}', config[key])
        return html

class HTMLGenerator:
    @staticmethod
    @ErrorHandler.with_error_handling
    def generate_html_pages(input_dir, output_dir, layout, config):
        for md_file_name in os.listdir(input_dir):
            md_file_path, html_file_path = FileOperations.get_file_paths(md_file_name, input_dir, output_dir)
            if os.path.isfile(md_file_path): 
                FileOperations.write_html_content(md_file_path, html_file_path, layout, config)

class DependenciesManager:
    @staticmethod
    def get_dependencies(input_dir, layout_path, config_file_path):
        return (
            input_dir, 
            FileOperations.create_output_dir(input_dir), 
            FileOperations.read_html_file(layout_path), 
            YAMLBuilder.create_from_file(config_file_path).get_mapping_from_file()
        )

class Jekyll:
    @staticmethod
    def generate_site(input_dir, layout_path, config_file_path):
        HTMLGenerator.generate_html_pages(*DependenciesManager.get_dependencies(input_dir, layout_path, config_file_path))

```

---

## How the Pipeline Flows

1. **Dependency Inversion & Collection:** The `DependenciesManager` acts as the data assembler. It reads your site settings via the custom YAML parser and pulls your base HTML theme template layout.
2. **Directory Mapping:** The `FileOperations` engine reads through your `.md` posts and constructs corresponding paths targets for your final build directory.
3. **Template Token Hydration:** The `HTMLRenderer` looks for explicit `{{ site.content }}` tags to inject your converted Markdown bodies and iterates through custom keys like `{{ site.title }}` or `{{ site.author }}` provided by your configuration mapping.

## Key Takeaways

By structuring a static site generator this way, we gain a few massive advantages:

* **Zero External Dependencies:** No need to debug broken third-party library updates.
* **Single Responsibility Principle:** Changing how markdown parses will never break the directory logic or error-handling code.
* **Stateless Execution:** Using `@staticmethod` utilities turns our site generator into a deterministic data pipeline. Input your files, get a perfect site every time.

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>