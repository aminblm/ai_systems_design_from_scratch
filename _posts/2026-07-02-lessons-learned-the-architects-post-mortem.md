---
layout: default
title: "Lessons Learned: The Architect’s Post-Mortem"
description: "Why senior engineers prioritize 'Lessons Learned' sessions. Learn how to transform technical failures into institutional knowledge using a structured post-mortem framework."
---

Author: **Amin Boulouma**, *Software Engineer*
**Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
**Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# Lessons Learned: The Architect’s Post-Mortem

Early in my career, I viewed a system outage as a personal failure—something to hide, patch, and move on from. I was wrong. In enterprise-grade software, a failure isn't an inconvenience; it is the most valuable piece of data you have. 

"Lessons Learned" is not just a meeting. It is a **feedback loop** that prevents the same technical debt from killing your project twice.

***

### The Problem: Knowledge Silos
When things go wrong, we often fix the symptom (e.g., "restart the server") and ignore the cause (e.g., "the connection pool wasn't configured for peak concurrency"). Without a structured post-mortem, the team remains in the dark, doomed to repeat the outage.



***

### Glossary for Beginners
* **Post-Mortem:** A formal process for analyzing why a system failed after the fact.
* **Blameless Culture:** An environment where failures are treated as technical issues rather than human errors.
* **Institutional Knowledge:** Information captured by the organization so that the team doesn't "forget" how to solve a recurring problem.

***

### Implementation: The Post-Mortem Framework
To make these sessions productive, I use a standard structure in my team. We keep it to three distinct sections.

```python
# A simple template to capture lessons learned programmatically
class PostMortem:
    def __init__(self, incident_id):
        self.incident_id = incident_id
        self.timeline = []
        self.root_causes = []
        self.action_items = []

    def add_event(self, timestamp, event):
        self.timeline.append((timestamp, event))

    def identify_root_cause(self, cause):
        # We focus on *why*, not *who*
        self.root_causes.append(cause)

    def add_remediation(self, action):
        self.action_items.append(action)

# Usage
post_mortem = PostMortem("INC-992")
post_mortem.identify_root_cause("Unbounded retry logic leading to thundering herd")
post_mortem.add_remediation("Implement Exponential Backoff with Jitter")

```

### Complex Example: Why we choose this over "Ad-hoc" fixing

Ad-hoc fixing is emotional. Structured learning is empirical. By documenting the incident, we defend our architecture choices in future audits.

```python
class IncidentAggregator:
    """
    Production-grade tracking of systemic issues.
    """
    def __init__(self):
        self.registry = {}

    def log_failure(self, category, fix_applied):
        # Tracking recurrence helps prioritize what to refactor
        if category not in self.registry:
            self.registry[category] = 0
        self.registry[category] += 1
        print(f"Logged {category}. Frequency: {self.registry[category]}")

# When a category hits a threshold, we know it's time for an architecture overhaul
aggregator = IncidentAggregator()
aggregator.log_failure("MemoryLeak", "Patch A")
aggregator.log_failure("MemoryLeak", "Patch B") # Frequency 2: Time to refactor!

```



### Quick Reference: The Post-Mortem Checklist

| Stage | Objective | Goal |
| --- | --- | --- |
| **Timeline** | What happened and when? | Establish objective facts. |
| **Root Cause** | Why did it happen? | Go 5-levels deep on "Why". |
| **Action Items** | How do we prevent it? | Assign tasks with due dates. |
| **Documentation** | Where do we save this? | Accessible knowledge base. |



### Developer Checklist: Is your process effective?

* [ ] **Blameless?** Is the focus on the system, not the individual?
* [ ] **Actionable?** Are there specific tickets assigned to fix the root cause?
* [ ] **Accessible?** Is the "Lessons Learned" document easy to find for new hires?
* [ ] **Recurring?** Did we check if this issue has happened before?

### Takeaway

The most senior engineers are the ones who have broken the most systems. The difference is that they **document the breakage**. When you treat your failures as a curriculum rather than a shame, you stop being a programmer and start being an architect. Stop fixing servers; start fixing the process that caused them to fail.
