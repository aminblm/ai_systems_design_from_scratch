---
layout: default
title: "The Zero-Dependency File Watcher: Building Lightweight Live-Reloading"
description: "How to implement a robust, cross-platform file system monitor using pure Python to enable real-time development cycles."
---

- Author: **Amin Boulouma**, *Software Engineer*
- **Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
- **Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# The Zero-Dependency File Watcher: Real-Time Development

When building an AI kernel, you need the system to detect code changes and perform hot-reloads instantly. Many engineers reach for heavy dependencies like `watchdog`. **This is an anti-pattern for internal tooling.** Third-party dependencies rot, introduce security vulnerabilities, and bloat your environment. A "Pipeline of One" should rely on pure, standard-library Python.

### Glossary for the Young Engineer
* **Zero-Dependency:** A program that doesn't need to download or install any extra "add-on" software to work. It’s like a chef who only uses tools already in their kitchen.
* **Polling:** The act of constantly checking "Did anything change yet?" every few seconds, just like checking the mailbox.
* **os.walk:** A powerful Python tool that lets you look through every folder and file inside a big folder, like a detective searching every room in a house.
* **Daemon:** A background process that works silently while you do other things. It’s like a little robot helper.

## The Problem: Dependency Bloat
Adding a massive library just to watch a few files for changes is architectural overhead. In a high-stakes environment, every dependency is a potential supply-chain attack vector. By using `os.walk` and `mtime` (Modification Time), we gain the same functionality in under 50 lines of code.



**Why we choose `os.walk` over OS-level events:** While OS events (`inotify`) are faster, they are **platform-dependent** (what works on Linux may fail on Windows). `os.walk` works everywhere and is simple enough to debug when things go wrong.

## Implementation

### Simple Example: The Basic Scanner
This snippet scans a folder and checks if files have been updated.

```python
import os
import time

def scan(path):
    return {p: os.path.getmtime(p) for p, _, f in os.walk(path) for f in f}

state = scan("./kernel")
# In a loop: compare with new_state = scan("./kernel")

```

### Complex Example: Production-Grade Daemon

This implementation runs in a separate thread and safely triggers a callback, making it suitable for hot-reloading your AI modules.

```python
import os
import time
import threading

class ZeroDepWatcher:
    def __init__(self, path, interval=1):
        self.path = path
        self.interval = interval
        self._state = self._scan()

    def _scan(self):
        return {os.path.join(r, f): os.path.getmtime(os.path.join(r, f)) 
                for r, _, files in os.walk(self.path) for f in files if f.endswith(".py")}

    def watch(self, callback):
        """Runs as a background daemon."""
        while True:
            time.sleep(self.interval)
            current = self._scan()
            
            # Detect new or modified files
            for path, mtime in current.items():
                if path not in self._state or mtime > self._state[path]:
                    callback(path)
            
            self._state = current

# Usage: threading.Thread(target=watcher.watch, args=(on_change,), daemon=True).start()

```

## Quick Reference: Polling vs. OS Events

| Feature | OS Events (e.g., inotify) | Pure Polling |
| --- | --- | --- |
| **CPU Usage** | Negligible | Low (with proper intervals) |
| **Complexity** | High (Platform specific) | Extremely Low |
| **Portability** | Limited | Universal (Any Python OS) |
| **Best For** | Massive filesystems | Small kernels/Development hot-reload |

## Developer Checklist

* [ ] **Daemonize**: Is the watcher running in a background thread so it doesn't block the main server?
* [ ] **Filtering**: Are you excluding hidden files (like `.git` or `__pycache__`) to save resources?
* [ ] **Error Handling**: Does the callback catch exceptions so a bad reload doesn't crash the watcher?
* [ ] **Clean Exit**: Does your system stop the thread on `SIGTERM`?

## Final Takeaways

1. **Dependencies are liabilities.** If you can solve it with the Python Standard Library, do it.
2. **Polling is predictable.** It is easy to debug, easy to rate-limit, and works exactly the same on a laptop as it does in a server container.
3. **Decouple the logic.** Keep the file-watching code separate from your business logic so you can swap it out later if you ever actually need OS-native performance.
