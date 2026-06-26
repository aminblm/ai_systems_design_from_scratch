---


title: "Orchestrating Workflows with Directed Acyclic Graphs (DAGs)"
description: "Learn how to manage complex task dependencies and execution timing using a Directed Acyclic Graph (DAG) scheduler."
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



# Orchestrating Workflows: The DAG Scheduler

<div class="author-card">
    <p><strong>Amin Boulouma</strong>,  <i>Software Engineer</i></p>
</div>


In distributed systems and automation pipelines, tasks rarely run in total isolation. Often, Task B requires the output of Task A, and Task C must only trigger if Task B completes successfully. A **Directed Acyclic Graph (DAG)** is the standard data structure to model these constraints.

## The DAG Architecture

A DAG is a graph composed of nodes (tasks) and edges (dependencies), where the "acyclic" property is strictly enforced to prevent infinite loops (where Task A depends on B, B on C, and C back on A).



### Core Components
* **`Task`**: The unit of execution, holding the callable logic, timing interval, and a set of `upstream_dependencies`.
* **`DAG`**: The container that maintains structural integrity. It uses an adjacency list (`downstream_edges`) to understand the flow of work.
* **`EngineScheduler`**: The "clock" of the system. It continuously evaluates the graph to determine which tasks are ready to run based on time and dependency resolution.

## Structural Integrity: Cycle Detection

The `validate_graph` method is a critical safeguard. Without it, a circular dependency could cause your engine to wait indefinitely, as no task would ever be "satisfied."

Using **Depth-First Search (DFS)** with a `rec_stack` (recursion stack), the algorithm identifies if a node is revisited while still in the current traversal branch, the definitive indicator of a cycle.

## Non-Blocking Execution Strategy

A common failure in schedulers is the "Stop-the-World" bug, where a slow task blocks the scheduler's ability to check other tasks. The `EngineScheduler.step()` method avoids this by:

1.  **Chronological Filtering**: Checking `_is_run_due()` to see if a task *needs* to run.
2.  **Dependency Resolution**: Using `_dependencies_satisfied()` to verify if the task *can* run.
3.  **Exception Isolation**: Wrapping `task.execute_func()` in a `try-except` block to ensure that a failing task doesn't crash the entire orchestration loop.

## Best Practices

* **Determinism**: Ensure that your DAG structure is defined *before* the scheduler starts. Modifying the graph at runtime can lead to race conditions.
* **Idempotency**: Since a scheduler might retry failed tasks, ensure that your `execute_func` can be run multiple times safely without leaving the system in a corrupted state.
* **Tick Rate Tuning**: The `tick_rate_seconds` in `run_forever` should be balanced. A rate that is too high wastes CPU cycles; a rate that is too low increases the latency between a dependency being met and the subsequent task starting.

By leveraging DAGs, you transition from fragile, linear scripts to robust, dependency-aware automation engines. The structure itself becomes the logic, making complex workflows predictable and easy to reason about.

{% raw %}


<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

{% endraw %}

