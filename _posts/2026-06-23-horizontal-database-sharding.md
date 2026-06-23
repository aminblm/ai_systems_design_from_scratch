---
title: Implementing Horizontal Database Sharding
description: Learn how to distribute data across clusters using consistent hashing and structural routing.
layout: default
---

# Horizontal Database Sharding

Horizontal sharding is the strategy of splitting a single dataset across multiple nodes (shards) to achieve horizontal scalability. Moving from simple list-based indexing to a structural routing paradigm using consistent hashing ensures your architecture can grow dynamically without manual data migration.

## The Core Mechanism: Consistent Hashing

The mathematical foundation of sharding is the mapping of an item's unique identifier to a specific shard index. Using the modulo operator ($n = \text{hash}(ID) \pmod{\text{Total Shards}}$) provides a deterministic way to find an item's location.



### Implementing Structural Routing

Instead of hardcoding lists, we route incoming data through a dedicated method that calculates the target shard dynamically.

```python
class ShardingRouter:
    def __init__(self, num_shards: int):
        self.shards = [Shard(id=i) for i in range(num_shards)]

    def _get_shard_route(self, val: str) -> Shard:
        """Determines the target shard using consistent hashing."""
        # Ensure consistent distribution using the modulo operator
        target_shard_idx = hash(str(val)) % len(self.shards)
        return self.shards[target_shard_idx]

    def add_item(self, val: str):
        shard = self._get_shard_route(val)
        shard.insert(val)

```

---

## Why Structural Routing Wins

1. **Uniform Distribution**: Consistent hashing prevents "hot shards" where one node becomes overloaded while others remain idle.
2. **Scalability**: By encapsulating the routing logic, you can transition to more complex algorithms (like Ketama hashing or jump consistent hash) without changing the business logic that consumes the data.
3. **Predictability**: Because the mapping is mathematical, you never need to query a central "directory" to find where a record lives—you simply calculate its address.

---

## Sharding Strategies

| Strategy | Logic | Pros | Cons |
| --- | --- | --- | --- |
| **Range-based** | By date or value range | Easy to query ranges | Creates uneven hotspots |
| **Hash-based** | Modulo of ID/Key | Uniform distribution | Resharding is expensive |
| **Directory-based** | Lookup table | Flexible routing | Central point of failure |

---

## Best Practices

* **Avoid Resharding**: Increasing the number of shards requires moving existing data. Use "virtual nodes" (placing multiple tokens per shard) to minimize data movement if you need to scale the cluster later.
* **Idempotency**: Ensure your sharding key is immutable. If the value used for the hash changes, the record effectively "disappears" because it will be mapped to the wrong shard.
* **Monitor Load**: Even with good hashing, some keys may have high frequency. Complement your sharding strategy with local caching to absorb "hot key" pressure.

---

By delegating placement to a structural routing paradigm, you build a system where data distribution is an inherent property of the architecture, not an administrative afterthought.

---