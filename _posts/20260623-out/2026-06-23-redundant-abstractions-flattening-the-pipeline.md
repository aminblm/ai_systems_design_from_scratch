---

title: "Defeating Redundant Abstraction - Simplifying Your Pipeline"
description: "Learn to recognize and eliminate 'layering rot' by flattening redundant classes and simplifying your data transformation pipelines."
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



# Redundant Abstractions: Flattening the Pipeline


<div class="author-card">
    <p><strong>{{ site.author.name }}</strong> — <i>{{ site.author.bio }}</i></p>
</div>


In software engineering, we often feel that "more classes mean better design." However, when you see a pipeline containing `MarkdownToHTMLBuilder`, `MarkdownToHTML`, and `HTMLGenerator`, you aren't looking at "clean design"—you are looking at **Redundant Abstraction**.

These layers exist as a web of dependencies, forcing the developer to track state and data passing through multiple wrappers that provide no actual benefit. This is a classic case of **"layering rot"**—where the architecture becomes a burden to the task it is supposed to perform.

## The Problem: Cognitive Overload
A simple pipeline—transforming text into HTML—should be straightforward. When you add three layers of indirection, you force anyone reading the code to hold the entire "web of dependencies" in their head just to trace a single string transformation.



### Why It Fails
* **Opaque Data Flow**: It is unclear which class is responsible for the actual transformation logic.
* **Maintenance Tax**: If the parsing requirement changes, you have to propagate that change through three different class interfaces.
* **Performance Overhead**: Frequent object instantiation and string copying across layers degrade performance without adding value.

---

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

