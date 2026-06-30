---

title: "Implementing Middleware: Building Flexible Socket Pipelines"
description: "How to use the Chain of Responsibility pattern to decouple cross-cutting concerns in your socket server."
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


<a href="https://www.producthunt.com/products/ai-systems-design-from-first-principles?embed=true&amp;utm_source=badge-featured&amp;utm_medium=badge&amp;utm_campaign=badge-ai-systems-design-from-first-principles" target="_blank" rel="noopener noreferrer"><img alt="AI Systems Design From First Principles - An implementation of AI Systems Design From First Principles | Product Hunt" width="250" height="54" src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1173628&amp;theme=dark&amp;t=1781635927239"></a>

{% raw %}

<div style="text-align: center; margin: 2rem 0; padding-bottom: 1rem; border-bottom: 1px solid #e9ebec;">
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">🏠 Documentation Hub</a>
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/blog" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">📝 Engineering Blog</a>
  <a href="https://github.com/aminblm/ai_systems_design_from_scratch" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">💻 GitHub Repository</a>
</div>

{% endraw %}


# Middleware: Building Flexible Socket Pipelines

{% raw %}

<div class="author-card">
    <p><strong>Amin Boulouma</strong>, <i>Software Engineer</i></p>
</div>

{% endraw %}



Middleware transforms a static server into a dynamic pipeline. Instead of hardcoding logic like logging, authentication, or payload transformation directly into your `SocketServer`, you delegate these responsibilities to a **chain of modular functions**.

## The Concept: Chain of Responsibility

Middleware allows you to intercept a request, perform an action, and decide whether to pass it to the next link in the chain or terminate the request early. 



## Why Use Middleware?

* **Separation of Concerns:** Your core server logic focuses on *handling* the socket connection, while middlewares handle *peripheral* tasks like header parsing, request sanitization, or request logging.
* **Declarative Configuration:** You can "plug and play" features. Need to add authentication? Just call `server.add_middleware(authenticate_request)`.
* **DRY (Don't Repeat Yourself):** Logic that is common across different request types is written once as a middleware and reused across the entire application.

## The Pipeline Flow

In the implementation provided, the request follows a strictly linear path:

1.  **Ingress:** The raw payload arrives from the socket.
2.  **Transformation (Middleware Chain):** Each registered middleware function receives the `request_text` and performs a transformation.
3.  **Core Logic:** The fully transformed string reaches the handler.
4.  **Egress:** The resulting output is returned to the client.

```python
# The Transformation Loop
for middleware in self._middlewares:
    request_text = middleware(request_text)

```

## Best Practices for Middleware Design

1. **Idempotency:** Try to ensure your middleware functions are predictable. Given the same input, they should reliably produce the same transformation.
2. **Order Matters:** In a middleware chain, the order of application is critical. For example, you must "decode" a payload before you "validate" the text format.
3. **Lightweight Processing:** Middleware runs for *every* request. Keep the logic inside these functions performant to ensure low latency.

## Summary: When to apply Middleware?

* **Logging/Observability:** Record metrics or request logs for every incoming connection.
* **Security:** Implement IP filtering, rate limiting, or authentication checks.
* **Data Sanitization:** Automatically strip sensitive characters, decode encoding schemes, or enforce character limits.

By treating your `SocketServer` as a pipeline rather than a monolith, you future-proof your network code against changing requirements.

{% raw %}

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

{% endraw %}

