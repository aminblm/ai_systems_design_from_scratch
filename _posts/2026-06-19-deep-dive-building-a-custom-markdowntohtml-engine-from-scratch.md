---
layout: default
title: "Deep Dive: Building a Custom Markdown-to-HTML Engine from Scratch"
description: "Learn how to write a lightweight, line-by-line Markdown parser using the Fluent Builder pattern and token-splitting logic without abstract syntax trees."
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


# Deep Dive: Building a Custom Markdown-to-HTML Engine from Scratch

In our previous post, we looked at how to orchestrate a static site generator pipeline using structural design patterns. Now, let’s zoom in on the most critical engine under the hood: the **Markdown Parser** (`MarkdownToHTMLBuilder`).

Writing a parser from scratch means bypassing heavy abstract syntax tree (AST) libraries and directly converting raw document lines into valid semantic HTML. Let’s break down how this specific internal component utilizes design patterns, object state manipulation, and explicit token parsing.

---

## The Design Pattern: The Fluent Builder

When constructing a compiler or a conversion tool, you don’t always know your data source up front. Sometimes you read a file directly from a disk, and other times you process an active in-memory text stream.

To solve this cleanly, the subsystem implements the **Builder Pattern** combined with a fluent interface. Notice how `MarkdownToHTMLBuilder` abstracts object creation away from the execution class (`MarkdownToHTML`):

```python
class MarkdownToHTMLBuilder:
    def __init__(self):
        self.markdown_file_path = ""
        self.markdown_text = ""

    def set_markdown_file_path(self, markdown_file_path):
        self.markdown_file_path = markdown_file_path
        return self  # Method chaining enabled here

    def set_markdown_text(self, markdown_text):
        self.markdown_text = markdown_text
        return self

    def build(self):
        return MarkdownToHTML(
            markdown_file_path = self.markdown_file_path,
            markdown_text = self.markdown_text,
        )

```

By returning `self`, the builder allows us to instantiate our markdown engine transparently through semantic static methods without complex positional arguments:

```python
# Reading from disk
engine = MarkdownToHTMLBuilder.create_from_file("posts/hello-world.md")

# Reading from raw memory string
engine = MarkdownToHTMLBuilder.create_from_text("# Quick Title")

```

---

## Token Standardization via Enums

Instead of cluttering string methods with hardcoded symbols (`""`, `"*"`), the framework maps special syntax markers using Python's native `Enum` system. This isolates changes to markdown syntax rules within a single structural point.

```python
from enum import Enum 

class MD_SPECIAL_CASES(Enum):
    BOLD = '**'
    ITALIC = '*'
    MULTILINE_CODE = '```'
    INLINE_CODE = '`'
    LINK = '[]()'
    IMAGE = '![]()'

```

---

## Line-by-Line Compilation Flow

The processing core uses a stateless pipeline approach inside `MarkdownParser.parse()`. Here is how a markdown document is split, evaluated, and compiled:

### 1. Front Matter Extraction

Jekyll files use YAML configurations bounded by triple dashes (`---`) at the top of the file. The helper uses structural lookahead arrays to bypass metadata initialization before processing semantic content:

```python
if lines[0].startswith('---'): 
    lines = Helpers._ignore_metadata_line(lines[1:])

```

### 2. Lexical Routing

Every single line goes through `_parse_line()`, which acts as a router matching prefixes to target HTML elements:

| Markdown Input Prefix | Target Parser Method | Output HTML Wrapper |
| --- | --- | --- |
| `# Title` | `_parse_header()` | `<h1>Title</h1>` |
| `> Quote` | `_parse_quote()` | `<blockquote>Quote</blockquote>` |
| `* Item` | `_parse_bullet_point()` | `<li>Item</li>` |
| ``code`` | `_parse_inline_code()` | `<pre><code>code</code></pre>` |

### 3. Inline Special Processing (Alternating Split Logic)

Parsing inline decorations like bold (``) or italic (`*`) without an official AST can be tricky. This codebase solves it creatively using array splits.

When you split a string by an inline token (e.g., text containing a single bolded word), the system splits the data into alternating indices:

* **Even Indexes (`i % 2 == 0`):** Represent standard text.
* **Odd Indexes (`i % 2 == 1`):** Represent text captured inside the special tokens.

```python
@staticmethod
def _parse_text_with_possible_bold(markdown_content):
    html_content = ""
    bold_split = markdown_content.split(MD_SPECIAL_CASES.BOLD.value)
    
    for i, bold_split_element in enumerate(bold_split): 
        if i % 2 == 1: 
            # Odd element means it sat between the '**' tokens!
            html_content += MarkdownParser._parse_bold_html_element(bold_split_element)
        else: 
            # Even element is passed down to check for italics nested inside
            html_content += MarkdownParser._parse_text_with_possible_italic(bold_split_element)
    return html_content

```

---

## Clean Architecture Benefits

By ensuring that `MarkdownParser` reads lists of strings and outputs single strings, we guarantee complete independence from file-system behavior. The parsing logic is deterministic and completely isolated:

1. **Testability:** You can easily pass arrays of mock strings directly into `MarkdownParser.parse()` to test styling rules without touching a hard drive.
2. **Extensibility:** If you want to add support for striking text (`~~`), you only need to update the `MD_SPECIAL_CASES` Enum and map a router step inside `_parse_line()`.
3. **Decoupled Architecture:** The file layout mechanics are managed by a custom `FileOperations` boundary wrapper, protecting your core string transformer from breaking if file access privileges change.

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>