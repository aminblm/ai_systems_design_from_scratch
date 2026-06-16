---
layout: default
title: "Building a Reactive Frontend Framework from Scratch"
description: "Demystifying component-based web architectures: Implementing a declarative state binder, component registry, and custom event dispatcher loop in pure Python."
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

<a href="https://www.producthunt.com/products/ai-systems-design-from-first-principles?embed=true&amp;utm_source=badge-featured&amp;utm_medium=badge&amp;utm_campaign=badge-ai-systems-design-from-first-principles" target="_blank" rel="noopener noreferrer"><img alt="AI Systems Design From First Principles - An implementation of AI Systems Design From First Principles | Product Hunt" width="250" height="54" src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1173628&amp;theme=dark&amp;t=1781635927239"></a>

<div style="text-align: center; margin: 2rem 0; padding-bottom: 1rem; border-bottom: 1px solid #e9ebec;">
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">🏠 Documentation Hub</a>
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/blog" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">📝 Engineering Blog</a>
  <a href="https://github.com/aminblm/ai_systems_design_from_scratch" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">💻 GitHub Repository</a>
</div>

# Building a Reactive Frontend Framework from Scratch

Modern client-side web development is dominated by component-driven frameworks like React, Vue, and Angular. These platforms abstract away direct, tedious DOM manipulations by introducing high-level software design patterns: **Component Isolation**, **Data Binding**, and **Decoupled Event Dispatching**. Instead of writing imperatively, you declare your state, and the core engine reflects those data states dynamically onto the user interface view.

But beneath the heavy Javascript bundle sizes and Virtual DOM nodes, how do these systems operate from first principles? 

To honor our repository's **strict zero-dependency constraint**, we will peel back the browser layer entirely. We will build a complete, state-bound frontend rendering engine prototype using nothing but standard Python objects.

---

## The Frontend Engine Architecture

Our custom system divides state tracking and UI rendering across four explicit structural roles:
1. **`Component`**: The baseline atomic module housing localized metadata, state definitions, and template hook pointers.
2. **`DataBinder`**: The state coordinator that maps raw component states into structured virtual UI nodes.
3. **`EventDispatcher`**: The centralized observer bus allowing modular decoupling of behavior execution from structural state mutation.
4. **`UI`**: The orchestration interface binding the individual sub-modules together into a clean API loop wrapper.

Here is the complete implementation block:

```python
class Component:
    def __init__(self, name, data=None, methods=None):
        self.name = name
        self.data = data if data is not None else {}
        self.methods = methods if methods is not None else {}
        self.events = {}

    def __repr__(self):
        return f'Component ({self.name}, data={self.data}, methods={self.methods})'


class DataBinder:
    def __init__(self):
        self.components = {}
        self.rendered = []

    def add_component(self, component):
        """Registers a detached UI component blueprint into active tracking state."""
        self.components[component.name] = component 

    def render(self):
        """Triggers a clean rendering tree pass over all tracked components."""
        self.rendered = []
        for component in self.components.values(): 
            self._render_component(component)
        return self.rendered

    def _render_component(self, component):
        """Simulates browser DOM string parsing by resolving state markers."""
        dom = f"<div id='{component.name}'>{component.data['text']}</div>"
        self.rendered.append(dom)
        return dom


class EventDispatcher:
    def __init__(self):
        self.listeners = {}

    def add_listener(self, event_type, handler):
        """Binds an execution handler function pointer to a targeted event key."""
        self.listeners[event_type] = handler 

    def trigger_event(self, event_type, data):
        """Fires an action message down the bus to evaluate registered event handlers."""
        handler = self.listeners.get(event_type)
        if handler: 
            handler(data)
    

class UI:
    def __init__(self):
        self.data_binder = DataBinder()
        self.event_dispatcher = EventDispatcher()

    def create_component(self, name, data=None, methods=None):
        """Convenience factory to initialize a node and link it to the data binder."""
        component = Component(name, data, methods)
        self.data_binder.add_component(component)
        return component

    def bind_data(self, component, key, value):
        """Mutates a target state component property to flag data adjustments."""
        component.data[key] = value

    def run(self):
        """Executes the render pipeline cycle and dumps resulting tree templates to standard out."""
        self.data_binder.render()
        print("Rendered UI:")
        for html in self.data_binder.render():
            print(html)


if __name__ == "__main__":
    ui = UI()
    
    # Example: create an active button component structure
    button = ui.create_component("button", {"text": "Click Me"}, {"click": ui.event_dispatcher.trigger_event})
    
    # Programmatically mutate state boundary values
    ui.bind_data(button, "text", "Hello world!")
    
    # Run structural pipeline compilation
    ui.run()

```

---

## Architectural Mechanisms Breakdown

### 1. Isolated Component Encapsulation

The `Component` class maps directly to the design patterns behind modern framework design. By storing properties inside a distinct dictionary boundary (`self.data`), states stay highly contained. Changing properties on a `button` node cannot trigger unintended adjustments across adjacent modules, mitigating global mutation risks.

### 2. The Declarative Render Pipeline

In old imperative programming setups, updating text forced a manual lookup string call like `document.getElementById('button').innerText = "New Text"`. Our `DataBinder` implements a primitive rendering pipeline. The `_render_component` helper acts as a template parser:

```python
dom = f"<div id='{component.name}'>{component.data['text']}</div>"

```

The underlying text is pulled straight from the component's state memory block. When `ui.run()` triggers its compile loop, it renders the HTML structure dynamically using whatever parameters are stored inside the data dictionary at that exact frame moment.

### 3. Decoupled Behavior Dispatching

Rather than tightly coupling execution statements to individual components, the system delegates actions through the `EventDispatcher`. The engine registers function handles within a tracking dictionary bus (`self.listeners`). When user triggers roll in, the target method is pulled dynamically and fired, preserving clear decoupling between interface elements and background business logic handlers.

---

## Framework Verification and Execution

When you run this framework module inside your terminal instance, it demonstrates how shifting data configurations changes the final UI layout automatically:

```bash
python py_frontend.py

```

### Expected Output Log

```text
Rendered UI:
<div id='button'>Hello world!</div>

```

Notice that although the `button` instance was initialized with a default text property of `"Click Me"`, invoking `ui.bind_data(button, "text", "Hello world!")` overwrote that state memory cell before the rendering pipeline step commenced. The engine compiled the accurate output data representation cleanly without hardcoded string alterations.

---

## Next Evolutionary Milestones

While this pattern demonstrates component initialization and data lookup mechanisms, it operates as a pull-based framework—meaning rendering only occurs when we manually invoke the `run()` system method.

To upgrade this framework into a highly interactive, push-based client emulator, our architecture roadmap highlights these feature enhancements:

* **True Reactive Listeners (Getters/Setters):** Wrapping `Component.data` using Python's magic properties or a Proxy setter class to intercept modifications, instantly calling the data binder's render function automatically whenever a value shifts.
* **Component Tree Nesting:** Enhancing the `DataBinder` to handle components nesting inside other components (`parent_component.children`), building an authentic, hierarchical virtual tree architecture.
* **Diffing Algorithm Implementation:** Building a tree difference algorithm that evaluates new output structures against cached render logs, updating only the elements that shifted rather than re-compiling the entire layout tree on every state update.
