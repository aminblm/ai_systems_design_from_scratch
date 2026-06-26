---
layout: default
title: "Parsing Site Configurations with a Custom YAML Engine"
description: "How to implement a deterministic, stateless string-slicing configuration engine to map global site configuration metadata without external packages."
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


# Parsing Site Configurations with a Custom YAML Engine

<div class="author-card">
    <p><strong>Amin Boulouma</strong>,  <i>Software Engineer</i></p>
</div>

We have successfully covered site orchestration and markdown translation. The final crucial pillar of our minimalist Jekyll engine is **Configuration Mapping**.

In a traditional setup, you would grab `PyYAML` or a similar heavy dependency. But remember our engineering constraint: **zero external dependencies**. To handle site configurations like title, author, or theme variables, we can build a lightweight key-value string mapper using the Fluent Builder interface we established earlier.

Let’s dissect how `YAMLBuilder` works to parse global configurations.

---

## Symmetry in System Architecture

One mark of a clean codebase is architectural consistency. By replicating the exact structural lifecycle we used for the Markdown parser, the learning curve across our codebase drops to zero.

Our YAML configuration processor is split into identical, distinct boundaries:

1. **`YAMLBuilder`**: Manages initialization parameters (fluent method chaining).
2. **`YAML`**: Holds instance data and exposes structural endpoints.
3. **`YAMLParser`**: A stateless engine dedicated solely to lexical transformation.

This design parity keeps components modular and highly predictable.

---

## Analyzing the Configuration Source Code

```python
from ai_systems_design.utils import FileOperationsUtility

class FileOperations:
    @staticmethod
    def read_yaml_file(yaml_file_path): 
        return FileOperationsUtility.read_decoded(yaml_file_path)

class YAMLBuilder:
    def __init__(self):
        self.yaml_file_path = None
        self.yaml_text = None

    def set_yaml_file_path(self, yaml_file_path):
        self.yaml_file_path = yaml_file_path
        return self

    def set_yaml_text(self, yaml_text):
        self.yaml_text = yaml_text
        return self
    
    def build(self):
        return YAML(self.yaml_file_path, self.yaml_text)

    @staticmethod
    def create_default():
        return YAMLBuilder().build()
    
    @staticmethod
    def create_from_file(yaml_file_path):
        return YAMLBuilder().set_yaml_file_path(yaml_file_path).build()
    
    @staticmethod
    def create_from_text(yaml_text):
        return YAMLBuilder().set_yaml_text(yaml_text).build()

class YAMLParser:
    @staticmethod
    def parse(yaml_content):
        mapping = {}
        for line in yaml_content.split("\n"):
            line = line.strip()
            if not line: 
                continue
            else: 
                # Split key and value on the structural delimiter ': '
                mapping[line.split(': ')[0]] = line.split(': ')[1]
        return mapping

class YAML:
    def __init__(self, yaml_file_path=None, yaml_text=None):
        self.yaml_file_path = yaml_file_path 
        self.yaml_text = yaml_text
        self.mapping = {}

    def get_mapping_from_file(self):
        self.mapping = YAMLParser.parse(FileOperations.read_yaml_file(self.yaml_file_path))
        return self.mapping
    
    def get_mapping_from_text(self):
        self.mapping = YAMLParser.parse(self.yaml_text)
        return self.mapping
                
    def get(self, key):
        return self.mapping[key]

```

---

## Deconstructing the Lexical Splitting Loop

Because this specific implementation focuses on flat metadata dictionaries (e.g., configurations without complex nested arrays), the parser can leverage a lightning-fast line tokenizer.

```python
for line in yaml_content.split("\n"):
    line = line.strip()
    if not line: continue
    else: mapping[line.split(': ')[0]] = line.split(': ')[1]

```

When given a file containing standard site variable blocks:

```yaml
title: My Engineering Blog
author: Sarah Dev
url: localhost:4000

```

The string parser performs a direct split on the canonical `: ` structure:

* `line.split(': ')[0]` targets the dynamic config key (`title`).
* `line.split(': ')[1]` extracts the dynamic data mapping value (`My Engineering Blog`).

This dictionary is then returned directly to our `HTMLRenderer` token replacer, seamlessly matching the variable keys inside our template layouts (`{{ site.title }}`).

---

## Why This Works So Efficiently

* **Stateless String Slicing:** By leaving state preservation outside of `YAMLParser.parse`, parsing configurations creates absolutely no tracking side effects. It takes text strings, maps data arrays, and unloads memory immediately.
* **Storage Inversion:** The configuration data is safely stored directly in the `YAML` domain model object, allowing consumers to repeatedly check runtime values via `config.get('url')` without triggering expensive disk-read cycles.
* **Isolated File Access:** Just like our Markdown transformer, standard I/O mechanics are wrapped elegantly inside an isolated `FileOperations` context, abstracting file layout logic entirely away from core dictionary operations.

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>