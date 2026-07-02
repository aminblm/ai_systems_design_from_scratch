---
layout: default
title: "The Circuit Breaker Pattern: Stopping Cascading Failures Before They Start"
description: "Why your services are failing during traffic spikes and how to implement circuit breakers to preserve system stability."
---

- Author: **Amin Boulouma**, *Software Engineer*
- **Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
- **Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# The Circuit Breaker Pattern: Stopping Cascading Failures

It’s 3:00 AM. A minor network fluctuation occurs, causing a downstream service to lag. Your primary service, attempting to be "helpful," keeps retrying requests. Because every thread is waiting on that slow service, your primary service runs out of memory and crashes. The lag has now become a total outage. This is a **cascading failure**, and it is the primary killer of microservice architectures.

### Glossary for the Young Engineer
* **Cascading Failure:** When one small part of your system breaks, it knocks over everything else like a line of dominoes.
* **Circuit Breaker:** A safety switch that stops your computer from trying to talk to a broken service until it is fixed, just like a light switch that turns off power to prevent a fire.
* **Latency:** The time it takes for a message to go from one computer to another. Think of it as how long a letter takes to travel in the mail.
* **State:** The "memory" of a program. It’s like remembering what toy you were just playing with.

## The Problem Space: The "Helpful" Service Anti-Pattern
Engineers often assume that if a service is slow, the best solution is to retry. **This is counter-intuitive and wrong.** In high-scale systems, retrying against a struggling service is equivalent to a Denial of Service (DoS) attack on your own infrastructure.



**Why we choose Circuit Breakers over infinite Retries:** Retries increase load; Circuit Breakers reduce load. When a service is broken, the most professional thing you can do is stop bothering it and return an error or a cached value immediately.

## Implementation

### Simple Example: The Basic State Toggle
This simple class acts as a gateway that monitors health and cuts the connection if too many failures occur.

```python
class SimpleCircuitBreaker:
    def __init__(self):
        self.is_closed = True # Closed means traffic flows
        self.failure_count = 0

    def call(self, func):
        if not self.is_closed:
            return "Circuit open: skipping call"
        try:
            return func()
        except Exception:
            self.failure_count += 1
            if self.failure_count > 3:
                self.is_closed = False
            raise

```

### Complex Example: Production-Grade Circuit Breaker

A production-ready breaker must manage **Timeouts**, **Automatic Reset**, and **State Transitions** to allow the system to recover without manual intervention.

```python
import time

class ProductionCircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=10):
        self.threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = 0
        self.state = "CLOSED" # CLOSED, OPEN, HALF-OPEN

    def call(self, func):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF-OPEN"
            else:
                return {"status": "error", "message": "Circuit open"}

        try:
            result = func()
            self._reset()
            return result
        except Exception:
            self._record_failure()
            raise

    def _record_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.threshold:
            self.state = "OPEN"

    def _reset(self):
        self.failures = 0
        self.state = "CLOSED"

```

## Quick Reference: Resilience Strategies

| Strategy | Use Case | Why? |
| --- | --- | --- |
| **Retry** | Transient network blips | Fixes temporary "glitches." |
| **Circuit Breaker** | Downstream outages | Stops traffic to failing services. |
| **Bulkhead** | Resource isolation | Prevents one service from hogging all memory. |

## Developer Checklist

* [ ] **Thresholds**: Are failure thresholds tuned to the specific service SLA?
* [ ] **Recovery Time**: Does the `recovery_timeout` allow the downstream service enough time to reboot?
* [ ] **Monitoring**: Are there alerts for when the circuit switches to `OPEN`?
* [ ] **Fallback**: Does the circuit return a sensible default or cached value when open?

## Final Takeaways

1. **Failing fast is a feature.** Protecting your system from itself is the definition of enterprise-grade engineering.
2. **Never retry indefinitely.** If a service is down, your retries are just making the recovery process harder for them.
3. **Automate the recovery.** Use `HALF-OPEN` states to test if a service is back online before resuming full traffic.
