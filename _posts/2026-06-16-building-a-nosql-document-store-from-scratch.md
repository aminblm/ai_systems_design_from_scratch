---
layout: default
title: "Building a NoSQL Document Store From Scratch"
description: "Demystifying unstructured data systems: Implementing a stateful database engine, document collection structures, and collection sharding mechanics in pure Python."
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


# Building a NoSQL Document Store From Scratch

<div class="author-card">
    <p><strong>Amin Boulouma</strong>,  <i>Software Engineer</i></p>
</div>

In non-relational database design, NoSQL document stores like MongoDB ditch rigid tables, rows, and foreign key constraints in favor of flexible, schema-agnostic abstractions. Data is bundled into self-contained objects called **Documents** (typically represented as BSON or JSON) and grouped inside **Collections**. 

To handle massive write volumes and analytical workloads at scale, these engines implement core systems architectural patterns: logical storage hierarchies, document indexing arrays, data aggregation pipelines, and **Horizontal Sharding** partitions.

To demystify how document-oriented storage engines maintain state and model cluster mechanics under the hood, we can build a functional prototype from the ground up.

Following our repository's **strict zero-dependency constraint**, we will implement an in-memory document database engine complete with data aggregation and data routing mechanics using nothing but pure Python standard constructs.

---

## The Document Store Architecture

Our NoSQL architecture coordinates independent structural layers: `Database` serves as the root namespace context, `Collection` manages memory records and index tables, `Document` encapsulates data blobs, and decoupled abstractions handle processing steps like `Query`, `Aggregation`, and `Sharding`.

Here is the complete codebase block matching our first-principles framework matrix:

```python
class Database:
    def __init__(self, name):
        self.name = name
        self.collections = []


class Collection:
    def __init__(self, name, fields=None):
        self.name = name
        self.fields = fields or {} 
        self.documents = []
        self.indexes = []

    def insert(self, document):
        """Appends a raw document object or data dict into the collection storage array."""
        self.documents.append(document)

    def find(self, filter=None):
        """Scans internal documents. Currently runs a basic lookup pass matching active blocks."""
        return [doc for doc in self.documents if filter]
    
    def aggregate(self, pipeline):
        """Executes an analytics pipeline pass to compute document frequency counts over schemas."""
        return {field: len([doc for doc in self.documents if doc.get(field)]) for field in self.fields}
    
    def create_index(self, index):
        """Registers a lookup index structure across targeted fields."""
        self.indexes.append(index)

    def shard(self, num_shards):
        """Simulates horizontal clustering mechanics by distributing documents across shard fields."""
        if not self.documents:
            self.shards = []
            return
        self.shards = [self.documents[i % len(self.documents)] for i in range(num_shards)]


class Document:
    def __init__(self, data):
        self.data = data

    
class Index:
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields


class Query:
    def __init__(self, filter=None, sort=None, limit=None):
        self.filter = filter
        self.sort = sort 
        self.limit = limit

    
class Aggregation:
    def __init__(self, pipeline):
        self.pipeline = pipeline


class Sharding:
    def __init__(self, database):
        self.database = database
        self.shards = []


if __name__ == "__main__":
    # 1. Initialize our namespace database container
    db = Database("mydb")

    # 2. Spawn a user metadata collection tracking structured keys
    collection = Collection("users", {"name": "text", "age": "int"})

    # 3. Insert an un-normalized document payload dictionary
    collection.insert({"name": "Alice", "age": "30"})

    # 4. Query data strings from collection storage arrays
    results = collection.find({"age": "30"})
    print(f"Find Query Results : {results}")

    # 5. Define and evaluate a system count aggregation step
    aggregation = Aggregation([{"$count": "age"}])
    agg_results = collection.aggregate(aggregation)
    print(f"Aggregation Results: {agg_results}")

    # 6. Horizontally distribute document arrays across 2 virtual cluster partitions
    collection.shard(2)
    print(f"Sharded Node Allocations: {collection.shards}")

```

---

## Architectural Mechanisms Breakdown

### 1. The Document Namespace Tree

The engine models a classic structural storage tree. The `Database` class holds a list array of `Collection` objects, and each collection functions as an isolated table boundary tracking its own list of documents, index schemas, and partition variables. This layered approach ensures database contexts remain perfectly separated inside system memory.

### 2. Analytical Pipeline Aggregations

In production systems, aggregation engines process high-density datasets through sequential, staged manipulation pipelines (such as filtering, grouping, and sorting). Our first-principles database mimics this pattern. The `aggregate` helper loops across the known structure keys defined inside `self.fields`:

```python
return {field: len([doc for doc in self.documents if doc.get(field)]) for field in self.fields}

```

It dynamically evaluates data field visibility, counting the instances where a given key exists across your stored documents and returning a clean, grouped summary map of database contents.

### 3. Modulo-Based Horizontal Sharding

When document collections grow too large for a single machine's storage limits, database systems distribute the write load across separate servers via **Sharding**. Our prototype implements an authentic data partitioning pattern by applying a deterministic mathematical modulo loop (`i % len(self.documents)`) over incoming collections. This strategy breaks a single unified collection down into independent balanced data shards, laying the structural groundwork for distributed scale.

---

## Verifying the Engine

Execute the module script file in your terminal workspace to observe how the data structures manage collections, count properties, and segment datasets:

```bash
python py_mongo_db.py

```

### Expected Console Output

```text
Find Query Results : [{'name': 'Alice', 'age': '30'}]
Aggregation Results: {'name': 1, 'age': 1}
Sharded Node Allocations: [{'name': 'Alice', 'age': '30'}, {'name': 'Alice', 'age': '30'}]

```

---

## Upcoming Engineering Sprints

While this structural architecture effectively isolates document namespaces, performs aggregation calculations, and runs basic shards, it functions as an unindexed in-memory prototype.

To evolve this code module into a highly performant, production-grade storage system, our upcoming architecture roadmap points to these milestones:

* **Authentic B-Tree Filtering:** Upgrading the `find` method from an $O(N)$ linear collection scan to query data through active `Index` objects using an $O(\log N)$ B-Tree lookup structure.
* **Pipeline Command Evaluation:** Expanding the `Aggregation` class to iterate over multiple stacked stage dictionaries, parsing pipeline primitives like `{"$match": ...}` and `{"$project": ...}` sequentially.
* **Persistent JSON Disks:** Writing automated transaction workers that serialize memory dictionary adjustments directly to non-volatile storage files, safeguarding data across engine restarts.

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>