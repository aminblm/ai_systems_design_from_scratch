---

title: "The Event Dispatcher: Decoupling Systems with the Observer Pattern"
description: "Learn how the Observer pattern enables decoupled communication between system components through a centralized Event Dispatcher."
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



# The Event Dispatcher: Decoupling via Multicast

{% raw %}

<div class="author-card">
    <p><strong>{{ site.author.name }}</strong> — <i>{{ site.author.bio }}</i></p>
</div>

{% endraw %}


In complex systems, components often need to communicate without being tightly bound to one another. Hard-coding dependencies (e.g., `ModuleA` calling `ModuleB` directly) creates a fragile, rigid architecture. The **Observer Pattern**, implemented here as an `EventDispatcher`, provides a clean solution: a centralized "broker" that manages communication between producers and consumers.

## The Problem: Tight Coupling
When your Git task logic must directly call your UI logic, your database logger, and your notification handler, every component becomes "aware" of every other component. If you change one, you risk breaking all.

## The Solution: The Multicast Observer Pattern

The `EventDispatcher` acts as a middleware. Producers "dispatch" events to the broker, and "subscribers" listen for events they care about. The producer doesn't know who—or even if—anyone is listening.

### Implementing the Broker
```python
class EventDispatcher:
    """An event broker implementing a standard multicast Observer pattern."""

    def __init__(self) -> None:
        self._listeners: Dict[str, List[Callable[[Any], None]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Any], None]) -> None:
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(handler)

    def dispatch(self, event_type: str, event_data: Any = None) -> None:
        handlers = self._listeners.get(event_type, [])
        if not handlers:
            logger.warning(f"Event '{event_type}' has no active subscribers.")
            return
            
        for handler in handlers:
            try:
                handler(event_data)
            except Exception as err:
                logger.error(f"Error in event '{event_type}': {err}")

```

## Why Decoupling Matters

1. **Independent Scalability**: You can add a new logger or a new analytics module by simply subscribing to an event, without modifying the existing business logic.
2. **Fault Isolation**: The `try-except` block inside the `dispatch` loop ensures that a crashing subscriber does not bring down the entire event-dispatching process.
3. **Extensibility**: The system becomes a "plug-and-play" architecture where you can attach new functionality at runtime.

## Best Practices

* **Keep Dispatcher Logic Simple**: The broker should only route traffic. Avoid adding complex business logic inside the `dispatch` loop itself.
* **Error Resilience**: Always wrap subscriber calls in `try...except` blocks. If one listener fails, it should never prevent other listeners from receiving the event.
* **Avoid Infinite Loops**: Be careful not to dispatch an event in a handler that listens for that same event, as this creates a recursive "event storm."

The `EventDispatcher` transforms your architecture from a rigid tree into a flexible, communicative network. It is the foundation for building systems that are truly modular and capable of evolving alongside your requirements.

{% raw %}


<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

{% endraw %}

