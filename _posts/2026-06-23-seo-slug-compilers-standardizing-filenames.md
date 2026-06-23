---
title: Building a Robust SEO Slug Compiler
description: Learn how to transform raw user input into web-safe, standardized Jekyll post filenames using normalization and character-set sanitization.
layout: default
---

# SEO Slug Compilers: Standardizing Filenames

For static site generators like Jekyll, the post filename is not just metadata—it is the URL structure. A proper filename must adhere to strict rules: no special characters, no spaces, and standardized date-prefixing. The `ResilientSlugGenerator` and `JekyllFilenameController` classes demonstrate a professional-grade pipeline for this task.

## The Normalization Pipeline

The conversion process is a multi-stage "purification" pipeline. Every step ensures the output becomes increasingly compliant with web URL standards.



1.  **Unicode Decomposition (NFKD)**: This is the most crucial step. It breaks down complex characters (like `é`) into their base characters (`e`) and combining accents, allowing them to be stripped during the ASCII conversion phase.
2.  **ASCII Sanitization**: Stripping non-ASCII characters ensures your URLs work across all browsers and server environments without encoding issues.
3.  **Regex Purging**: We use `re.sub(r'[^\w\s-]', '', text)` to remove any character that is not a word character (letters, numbers, underscores), a space, or a hyphen.
4.  **Token Normalization**: Finally, we collapse multiple spaces or hyphens into a single hyphen delimiter (`-`), resulting in clean tokens like `this-is-my-post`.

---

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

---

## Best Practices

* **Fail Fast**: If the input is empty or contains no alphanumeric characters, the engine informs the user immediately rather than generating a broken filename like `2026-06-23-.md`.
* **Idempotency**: The engine takes the same input and produces the same output every time, ensuring that even if you re-run the compiler, your file naming remains consistent.
* **Separation of Concerns**: The `ResilientSlugGenerator` is pure logic—it doesn't know about files, dates, or Jekyll. The `JekyllFilenameController` handles the "business logic" of how that slug fits into your project folder. This makes the generator highly reusable in other parts of your system.

---

By decomposing your slug generation into these modular steps, you create a system that is easily testable, highly predictable, and perfectly suited for automation.
