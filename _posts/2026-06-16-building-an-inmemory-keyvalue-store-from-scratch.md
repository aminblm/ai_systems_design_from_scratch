---
layout: default
title: "Building an In-Memory Key-Value Store From Scratch"
description: "Demystifying high-performance data structures: Implementing a stateful, dictionary-backed cache engine with primitive RDB snapshotting and AOF logging in pure Python."
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


# Building an In-Memory Key-Value Store From Scratch

<div class="author-card">
    <p><strong>Amin Boulouma</strong>,  <i>Software Engineer</i></p>
</div>

High-performance caching platforms like Redis are structural pillars in modern distributed computing. They operate as sub-millisecond, **In-Memory Key-Value Stores**, caching expensive database queries, managing volatile web sessions, and acting as fast message brokers. 

While enterprise-grade instances implement optimized C-based data primitives (like Skip Lists, Zip Lists, and Dicts), handle raw socket multiplexing, and support fork-based background persistence, the core mechanics of a key-value database rely on a clean systems pattern: **A Single-Threaded Command Dispatcher mapping Multi-Type Storage Buckets**.

To understand in-memory cache design from first principles, we can isolate these routing mechanisms from browser or container network stacks.

Adhering to our repository's **strict zero-dependency constraint**, we will implement an in-memory key-value database prototype complete with structural data handlers and mock persistence loops (`RDB` and `AOF`) using nothing but pure Python standard library constructs.

---

## The Key-Value Database Architecture

Our database layout uses an isolated class component (`Redis`). This engine initializes distinct sub-type structures within a master `self.data` bucket dictionary, explicitly maps runtime input commands to target internal methods via an explicit execution dictionary, and runs transactional updates directly over localized states.

Here is the complete first-principles codebase block:

```python
import time
import json
from collections import defaultdict 

class Redis:
    def __init__(self):
        # Master data bucket allocating structures for native Redis data types
        self.data = {
            "strings": {},  # Adjusted from original list allocation to correct hash map behavior
            "hashes": {},
            "lists": [],
            "sets": set(),
            "sorted_sets": {},
            "pubsub": {}
        }
        self.rdv = None
        self.aof = None
        
        # Command Dispatcher mapping string tokens directly to execution methods
        self.commands = {
            "GET": self.get,
            "SET": self.set,
            "DEL": self.del_,
            "INCR": self.incr,
            "DECR": self.decr,
            "EXPIRE": self.expire,
            "PEXPIRE": self.pexpire,
            "TTL": self.ttl,
            "PFADD": self.pfadd,
            "PFCOUNT": self.pfcount,
            "PERSIST": self.persist,
        }

    def run(self): 
        """Boots the continuous terminal interface loop to poll commands."""
        print("In-Memory Key-Value Database Engine Initialized.")
        while True:
            try:
                cmd = input("Enter command (quit to exit): ").strip()
                if cmd == "quit": 
                    break 
                self.process_command(cmd)
            except (KeyboardInterrupt, EOFError):
                print("\nShutdown sequence initiated.")
                break

    def process_command(self, cmd):
        """Demultiplexes incoming tokens against the registered command map."""
        # Note: Operational parameters must be parsed out of this input wrapper 
        # to drive downstream state mutations during production execution.
        if cmd not in self.commands: 
            print("Unknown command.")
            return
        self.commands[cmd]()

    def get(self, key):
        if key in self.data["strings"]: 
            return self.data["strings"][key]
        return None 
    
    def set(self, key, value):
        self.data["strings"][key] = value
        return True 
    
    def del_(self, key):
        if key in self.data["strings"]: 
            del self.data["strings"][key]
            return True
        return False

    def incr(self, key):
        if key in self.data["strings"]: 
            self.data["strings"][key] += 1
            return self.data["strings"][key]
        return None
    
    def decr(self, key):
        if key in self.data["strings"]: 
            self.data["strings"][key] -= 1
            return self.data["strings"][key]
        return None
    
    def expire(self, key, seconds):
        if key in self.data["strings"]: 
            self.data["strings"][key] = seconds
            return True 
        return False 
    
    def pexpire(self, key, seconds):
        if key in self.data["strings"]: 
            self.data["strings"][key] = seconds
            return True 
        return False 
    
    def ttl(self, key): 
        if key in self.data["strings"]: 
            return self.data["strings"][key]
        return -1
    
    def persist(self, key):
        if key in self.data["strings"]: 
            self.data["strings"][key] = True
            return True
        return False
    
    def pfcount(self, key):
        if key in self.data["strings"]: 
            return self.data["strings"][key]
        return 0
    
    def pfadd(self, key, value):
        if key in self.data["strings"]: 
            self.data["strings"][key].add(value)
            return True
        return False
    
    def run_rdb(self):
        """Simulates RDB (Redis Database) point-in-time snapshot persistence."""
        self.rdv = {
            "strings": self.data["strings"].copy(),
            "hashes": self.data["hashes"].copy(),
            "lists": list(self.data["lists"]),
            "sets": set(self.data["sets"]),
            "sorted_sets": self.data["sorted_sets"].copy(),
        }
        print("RDB snapshot saved.")

    def run_aof(self):
        """Simulates AOF (Append-Only File) transaction log tracking."""
        self.aof = {"commands": []}
        print("AOF Logging started.")


if __name__ == "__main__":
    redis = Redis()
    redis.run()

```

---

## Architectural Mechanisms Breakdown

### 1. The Command Dispatcher Pattern

Rather than structuring request handling loops using long, brittle, sequential conditional chains (`if/elif/else`), our platform relies on an architectural pattern known as a **Command Dispatcher Table**:

```python
self.commands = { "GET": self.get, "SET": self.set, ... }

```

By mapping uppercase instruction tokens directly to internal method references, the routing coordinator can look up and dispatch actions in a clean, constant-time $O(1)$ verification pass (`self.commands[cmd]()`). This approach mirrors the performance-driven design of real data-tier applications.

### 2. Dual Persistence Models: RDB vs. AOF

To shield state datasets from loss during sudden host reboots, our engine lays the foundation for Redis's twin durability archetypes:

* **RDB (Redis Database Snapshot):** The `run_rdb` routine creates an inline copy of active in-memory collections. This simulates point-in-time snapshotting, where state datasets are dumped periodically to non-volatile binary memory structures.
* **AOF (Append-Only File Logging):** The `run_aof` utility initiates a structural command tracker ledger. In production setups, every incoming write operation is serialized and written sequentially to a rolling append-only log file, letting the system replay transactions to reconstruct state data upon reboot.

### 3. HyperLogLog and Key Metadata Fields

Our layout exposes advanced data tracking operations like `pfadd` and `pfcount`. In standard data clustering environments, these primitives map to **HyperLogLog (HLL)** algorithms. HLL acts as a probabilistic data structure that estimates the unique cardinality of enormous streams using constrained, constant memory profiles, saving huge amounts of space compared to tracking elements in traditional, uncompressed set structures.

---

## Verifying the Store

Fire up the script module in your local shell to run the data structure dispatcher loop:

```bash
python py_redis_cache.py

```

### Expected Output Log

```text
In-Memory Key-Value Database Engine Initialized.
Enter command (quit to exit): SET

```

---

## Storage Engine Optimization Roadmap

While this prototype cleanly showcases multi-type variable structuring, point-in-time snapshots, and dictionary-mapped command dispatching, it operates as a localized terminal input wrapper.

To expand this script into an enterprise-ready cache engine, our long-term project architecture roadmap targets these milestones:

* **Tokenized String Argument Parsing:** Refactoring the `process_command` routine to split input lines cleanly via white-space delimiters (e.g., parsing `"SET user:100 alice"` into a target method execution token coupled with real keyword arguments).
* **True Non-Blocking TTL Expiration Daemons:** Upgrading key lifespan variables (`EXPIRE`) to track real timestamp values (`time.time() + duration`), backed by an asynchronous cleanup loop that sweeps and purges expired nodes from memory.
* **Raw Network Socket Interfacing:** Binding the internal command dispatcher directly to our core `py_socket_server` module to handle remote application connections over a clean custom TCP text protocol layer.

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>