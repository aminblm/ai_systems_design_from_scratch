---
layout: default
title: "Concurrency vs. Parallelism: Multiprocessing vs. Threading in Python"
description: "A deep dive into the architectural differences between multiprocessing and threading, and when to use each for high-performance Python applications."
---

# Concurrency vs. Parallelism: Multiprocessing vs. Threading

In high-performance system design, understanding how to leverage CPU resources is critical. A common point of confusion for engineers moving into concurrent systems is the distinction between **Threading** and **Multiprocessing**. While both allow tasks to run concurrently, they operate at fundamentally different levels of the operating system.

## The Architectural Divide

To understand the difference, we must look at how Python manages memory and CPU cycles.

* **Threading (Concurrency):** Threads exist within the same process and share the same memory space. In Python, the **Global Interpreter Lock (GIL)** ensures that only one thread executes bytecode at any given time. This makes threading ideal for **I/O-bound tasks** (waiting for network, disk, or user input), as threads can yield control while waiting.
* **Multiprocessing (Parallelism):** This approach spawns entirely new processes, each with its own Python interpreter and memory space. Because they exist in separate memory domains, they bypass the GIL entirely, allowing for true **parallelism** on multi-core processors. This is essential for **CPU-bound tasks** (data processing, numerical simulations, heavy parsing).

## Implementation Examples

### 1. Simple Example: I/O Bound Tasks (Threading)
Threads are lightweight and excellent for tasks where the CPU is mostly idle waiting for external responses.

```python
import threading
import time

def worker(name):
    print(f"Task {name} starting...")
    time.sleep(1)  # Simulate I/O wait
    print(f"Task {name} finished.")

# Threading usage
threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
for t in threads: t.start()
for t in threads: t.join()

```

### 2. Enterprise Example: CPU Bound Tasks (Multiprocessing)

For compute-intensive operations, we use `multiprocessing` to distribute the load across available CPU cores.

```python
import multiprocessing
import math

def compute_heavy(n):
    # Simulate CPU intensive math
    return sum(math.factorial(i) for i in range(n))

def run_parallel_jobs(data_list):
    # Use ProcessPoolExecutor or Pool to manage worker lifecycle
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(compute_heavy, data_list)
    return results

if __name__ == "__main__":
    # Example usage for large-scale data processing
    data = [1000, 2000, 3000]
    results = run_parallel_jobs(data)
    print(f"Computed {len(results)} results in parallel.")

```

## Summary for System Architecture

| Feature | Threading | Multiprocessing |
| --- | --- | --- |
| **Primary Use** | I/O-bound (network, disk) | CPU-bound (math, data, AI) |
| **Memory** | Shared | Isolated |
| **GIL** | Limited by GIL | Bypasses GIL |
| **Overhead** | Low | High (inter-process communication) |

When designing your next system, prioritize **Threading** for responsiveness in network-heavy applications, and reserve **Multiprocessing** for scaling compute-heavy pipelines across physical CPU cores.


**Author: Amin Boulouma, Software Engineer**
**Github source code: https://github.com/aminblm/ai_systems_design_from_scratch**
