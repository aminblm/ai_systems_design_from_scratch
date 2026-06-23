---
title: Orchestrating Workflows with Directed Acyclic Graphs (DAGs)
description: Learn how to manage complex task dependencies and execution timing using a Directed Acyclic Graph (DAG) scheduler.
layout: default
---

# Orchestrating Workflows: The DAG Scheduler

In distributed systems and automation pipelines, tasks rarely run in total isolation. Often, Task B requires the output of Task A, and Task C must only trigger if Task B completes successfully. A **Directed Acyclic Graph (DAG)** is the standard data structure to model these constraints.

## The DAG Architecture

A DAG is a graph composed of nodes (tasks) and edges (dependencies), where the "acyclic" property is strictly enforced to prevent infinite loops (where Task A depends on B, B on C, and C back on A).



### Core Components
* **`Task`**: The unit of execution, holding the callable logic, timing interval, and a set of `upstream_dependencies`.
* **`DAG`**: The container that maintains structural integrity. It uses an adjacency list (`downstream_edges`) to understand the flow of work.
* **`EngineScheduler`**: The "clock" of the system. It continuously evaluates the graph to determine which tasks are ready to run based on time and dependency resolution.

---

## Structural Integrity: Cycle Detection

The `validate_graph` method is a critical safeguard. Without it, a circular dependency could cause your engine to wait indefinitely, as no task would ever be "satisfied."

Using **Depth-First Search (DFS)** with a `rec_stack` (recursion stack), the algorithm identifies if a node is revisited while still in the current traversal branch—the definitive indicator of a cycle.



---

## Non-Blocking Execution Strategy

A common failure in schedulers is the "Stop-the-World" bug, where a slow task blocks the scheduler's ability to check other tasks. The `EngineScheduler.step()` method avoids this by:

1.  **Chronological Filtering**: Checking `_is_run_due()` to see if a task *needs* to run.
2.  **Dependency Resolution**: Using `_dependencies_satisfied()` to verify if the task *can* run.
3.  **Exception Isolation**: Wrapping `task.execute_func()` in a `try-except` block to ensure that a failing task doesn't crash the entire orchestration loop.

---

## Best Practices

* **Determinism**: Ensure that your DAG structure is defined *before* the scheduler starts. Modifying the graph at runtime can lead to race conditions.
* **Idempotency**: Since a scheduler might retry failed tasks, ensure that your `execute_func` can be run multiple times safely without leaving the system in a corrupted state.
* **Tick Rate Tuning**: The `tick_rate_seconds` in `run_forever` should be balanced. A rate that is too high wastes CPU cycles; a rate that is too low increases the latency between a dependency being met and the subsequent task starting.

---

By leveraging DAGs, you transition from fragile, linear scripts to robust, dependency-aware automation engines. The structure itself becomes the logic, making complex workflows predictable and easy to reason about.
