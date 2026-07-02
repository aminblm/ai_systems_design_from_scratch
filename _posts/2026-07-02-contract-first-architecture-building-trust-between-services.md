---
layout: default
title: "Contract-First Architecture: Designing Before Implementing"
description: "Why developing service APIs in isolation leads to failure and how to use Contract-First design to guarantee system interoperability."
---

- Author: **Amin Boulouma**, *Software Engineer*
- **Github source code**: [https://github.com/aminblm/ai_systems_design_from_scratch](https://github.com/aminblm/ai_systems_design_from_scratch)
- **Engineering Blog**: [https://aminblm.github.io/ai_systems_design_from_scratch/blog/](https://aminblm.github.io/ai_systems_design_from_scratch/blog/)

# Contract-First Architecture: Building Trust Between Services

In distributed systems, the most common cause of "integration hell" is **Code-First development**. This happens when teams write code, build an API, and *then* document it. You’ve likely experienced the aftermath: the "midnight deployment spike" where a minor change in the Order Service unexpectedly broke the Payment Service because the field types were silently changed.

**Contract-First Architecture** mandates that the API design—the "contract"—is finalized and agreed upon by all stakeholders *before* a single line of production code is written.



## The Theory: The API as a Source of Truth
The contract (usually defined in OpenAPI/Swagger or Protobuf) serves as the **source of truth**. Both the client and the server consume this contract to generate their respective codebases. This ensures that both sides are always in sync.

## Glossary for Beginners
* **Contract**: A formal agreement on how two computers talk to each other (e.g., "I will send you a number, and you will send me a text back").
* **API (Application Programming Interface)**: A waiter in a restaurant that takes your order to the kitchen and brings your food back.
* **Schema**: The blueprint or "form" that defines what data looks like.
* **Interoperability**: The ability of different systems to understand each other perfectly.


## Simple Implementation: Define and Validate
We define a schema and a validator to ensure the incoming data strictly adheres to our agreed-upon contract.

```python
# The Contract: A simple dictionary schema
CONTRACT = {
    "user_id": int,
    "amount": float
}

def validate_request(payload):
    for key, expected_type in CONTRACT.items():
        if key not in payload or not isinstance(payload[key], expected_type):
            raise ValueError(f"Contract violation: {key} must be {expected_type}")
    return True

```


## Complex Implementation: Schema-Driven Proxy

In a production-grade scenario, we use the contract to automatically gate-keep traffic.

```python
class ContractGateway:
    def __init__(self, schema):
        self.schema = schema

    def process(self, request_data):
        # Enforce contract before passing to internal services
        try:
            self._enforce(request_data)
            return self._forward_to_service(request_data)
        except ValueError as e:
            return {"status": "400", "error": str(e)}

    def _enforce(self, data):
        # Complex logic to check nested fields and constraints
        for field, rules in self.schema.items():
            if field not in data:
                raise ValueError(f"Missing field: {field}")
            # Additional logic for range, length, etc.

```

## Quick Reference: Contract-First vs. Code-First

| Feature | Code-First | Contract-First |
| --- | --- | --- |
| **Development Speed** | Faster initially | Slower initially (Design phase) |
| **Integration Risk** | High (Discovery at runtime) | Low (Discovery at design time) |
| **Documentation** | Often stale/outdated | Always accurate (Source of truth) |
| **Parallelization** | Low | High (Both teams code to the spec) |

## Why We Choose Contract-First over Code-First

We choose **Contract-First** because it forces engineers to think about **API surface area** before implementation. It eliminates the ambiguity that leads to "the midnight deployment spike." When the contract is the lead, you can generate mock servers for frontend teams to work against, even before the backend logic is finished.

## Developer Checklist

* [ ] Is the API schema stored in the repository?
* [ ] Is the schema validated at the edge (Gateway) before hitting internal services?
* [ ] Are breaking changes detected by CI via schema comparison?
* [ ] Do both frontend and backend teams have a stake in the contract definition?

### Takeaways

* **Design Intent**: Code is an implementation detail; the contract is the architecture.
* **Automate Truth**: Let the schema generate your client libraries and documentation.
* **Fail Early**: Catch incompatibility errors at build time, not during a production deployment.
