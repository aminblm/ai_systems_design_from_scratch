---
layout: default
title: "5 Lessons Learned from My First Real Python Struggle (Memory Leaks)"
description: "Python is deceptively simple. I share the story of my first major architectural struggle with memory management and how it changed my approach to building systems."
---

- Author: **Amin Boulouma**, *Software Engineer*
- **Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
- **Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# 5 Lessons Learned from My First Real Python Struggle (Memory Leaks)

I still remember the night my first "production" Python service died. It was a simple data processor—just a loop reading from a queue, performing a transformation, and writing to a database. It worked perfectly in staging. In production, however, it started slow, grew until the OS killed it, and then restarted. I had spent hours optimizing logic, but I had ignored one fundamental truth: Python is easy until you start fighting its memory management.

That experience taught me that Python’s "simplicity" is an abstraction. It handles memory for you, but if you treat it like a bottomless pit, you will eventually hit the wall.

***

### Glossary for Beginners

* **Memory Leak:** When your program allocates memory for objects but never releases them, causing your system's RAM to fill up until the program crashes.
* **Garbage Collector:** A background process in Python that automatically finds and removes objects that are no longer being used.
* **Circular Reference:** A situation where two objects refer to each other, which can sometimes trick the Garbage Collector into thinking they are still in use.
* **Profiler:** A tool that watches your code while it runs to tell you exactly how much memory or time each part of the program is using.

***

### The Architecture: Why We Should Care About Object Lifecycles

We prioritize **Object Lifecycle Management** because in long-running services (like background workers or API servers), even a tiny "leak" compounds. We chose to move away from global state and persistent dictionaries because they hold onto references indefinitely. By moving to scoped, transient objects, we ensure the garbage collector can do its job effectively.



***

### Simple Example: The Persistent List

A common way to leak memory is by appending to a global list and forgetting to clear it.

```python
# The Mistake: A list that grows forever
data_log = []

def process(item):
    data_log.append(item) # This list will eventually consume all RAM
    return item

# The Fix: Use a fixed-size buffer or clear the list
def process_fixed(item):
    if len(data_log) > 1000:
        data_log.pop(0)
    data_log.append(item)
    return item

```



### Complex Example: Production-Grade Resource Cleanup

In enterprise systems, you deal with external connections. If you don't explicitly close them, Python's GC might not reclaim the OS resources fast enough.

```python
import weakref

class DatabaseConnection:
    def close(self):
        print("Connection closed")

class Service:
    def __init__(self, connection):
        # Using a weak reference prevents the Service from 
        # keeping the connection alive longer than necessary
        self._connection = weakref.ref(connection)

    def run(self):
        conn = self._connection()
        if conn:
            print("Executing query...")
        else:
            print("Connection already closed")

# Deployment
conn = DatabaseConnection()
service = Service(conn)
service.run()
del conn # Connection becomes eligible for collection
service.run()

```


### Quick Reference: Memory Management Strategies

| Strategy | When to use | Why? |
| --- | --- | --- |
| **WeakRef** | Caching/Associations | Avoids preventing object destruction. |
| **Generators** | Large Datasets | Processes data one piece at a time. |
| **Context Managers** | External Resources | Ensures cleanup happens immediately. |
| **`__slots__`** | Millions of objects | Reduces object memory footprint. |



### Developer Checklist for Implementation

* [ ] **Limit Scope:** Keep object lifespans as short as possible.
* [ ] **Monitor Growth:** Use `tracemalloc` to track memory consumption during peak loads.
* [ ] **Avoid Globals:** If your service lives for days, global containers are your enemy.
* [ ] **Explicit Cleanup:** Use `with` statements for any resource that connects to the outside world.



### Takeaways & TL;DR

* **Python is not magic:** Just because it manages memory doesn't mean you can ignore it.
* **Objects want to die:** Help the garbage collector by removing references as soon as you are done with them.
* **Profile early:** Don't wait for a production crash to look at your memory usage.


### Counter-Intuitive Insight

The most common mistake is assuming that `del` deletes an object. It doesn't—it just deletes the **name** pointing to the object. The object only dies when its reference count hits zero. I spent weeks using `del` trying to "fix" my memory issues before realizing I had references hidden in long-lived objects. Stop trying to manually "delete" objects and start designing systems where objects naturally go out of scope.
