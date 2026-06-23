---
title: "In-Memory Data Stores: Implementing Redis-like TTL and Expiration"
description: "Learn how to manage Time-To-Live (TTL) metadata and lazy eviction strategies in an in-memory key-value store."
layout: default
---

# In-Memory Data Stores: Managing Expiration

In high-performance systems, an in-memory data store is often the backbone of temporary state management. Implementing features like `EXPIRE` and `TTL` (Time-To-Live) requires more than just storing values; it requires a robust strategy for **eviction**.

## The Architecture of Expiration

The `RealtimeRedisEngine` utilizes two core concepts to manage data lifecycle: **Timestamp-based Expiry** and **Lazy Eviction**.

### 1. The `RedisObject` Wrapper
Instead of storing raw values directly in the database dictionary, we wrap them in a `RedisObject`. This object holds the actual data along with an `expires_at` epoch timestamp. 



### 2. Lazy Eviction
Rather than running an expensive background "reaper" thread that constantly scans for expired items, we use **Lazy Eviction**. Every time a key is accessed via `_get_valid_obj`, the engine checks the `expires_at` timestamp. If the current time is past the expiry window, the object is treated as non-existent and immediately deleted.

```python
def _get_valid_obj(self, key: str) -> Optional[RedisObject]:
    obj = self._db.get(key)
    if obj and obj.is_expired():
        del self._db[key] # Pruning the expired entry on access
        return None
    return obj

```

---

## Command Lifecycle Routing

The `execute_command_string` method functions as a command dispatcher. It translates raw input strings (like `"SET mykey 100"`) into functional logic. By mapping tokens directly to class methods, we create a clean, extensible API that mimics the actual Redis protocol.

| Command | Logic |
| --- | --- |
| **SET** | Stores a new `RedisObject`. |
| **EXPIRE** | Calculates the absolute `time.time() + duration`. |
| **TTL** | Subtracts current time from `expires_at`. |
| **INCR** | Performs atomic increment on validated integer values. |

---

## Why Lazy Eviction Wins

1. **Efficiency**: We avoid "polling" the database. Expired items are cleaned up only when they are requested, spreading the overhead of deletion across your normal traffic.
2. **Simplicity**: It prevents complex locking scenarios that would be required if a background cleanup thread were constantly mutating the database dictionary.
3. **Accuracy**: By checking `time.time()` at the exact moment of access, we ensure that an item never appears "alive" after its expiration deadline.

---

## Best Practices

* **Handle Missing Data**: Always define clear return values for missing data. In Redis, `(nil)` indicates a missing key, while `-2` often signifies a key that has expired. Consistency in these responses is key to a stable API.
* **Type Safety**: Ensure your `INCR` logic handles non-integer types gracefully. A robust data store must protect its internal data consistency by catching type conversion errors before updating state.
* **Timestamp Precision**: Using `time.time()` provides a floating-point epoch. When calculating `TTL`, use `int(round(...))` to provide a human-readable integer response that matches the expected Redis output format.

---

By combining metadata wrappers with lazy eviction, you create a system that is memory-aware and architecturally resilient, capable of handling temporary state with minimal computational overhead.
