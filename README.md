<div style="text-align: center; margin: 2rem 0; padding-bottom: 1rem; border-bottom: 1px solid #e9ebec;">
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">🏠 Documentation Hub</a>
  <a href="https://aminblm.github.io/ai_systems_design_from_scratch/blog" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">📝 Engineering Blog</a>
  <a href="https://github.com/aminblm/ai_systems_design_from_scratch" class="btn" style="margin: 0.25rem; padding: 0.6rem 1rem; font-weight: normal; font-size: 0.9rem; background-color: #24292e; border-color: #24292e;">💻 GitHub Repository</a>
</div>

# AI Systems Design From Scratch 

[![Python Version](https://img.shields.io/badge/python-3.14.5-blue?logo=python&logoColor=white&style=flat-square)](https://www.python.org/)
[![Dependencies](https://img.shields.io/badge/dependencies-zero--mandate-success?style=flat-square)](#the-zero-dependency-mandate)
[![License](https://img.shields.io/badge/license-MIT-red?style=flat-square)](https://opensource.org/licenses/MIT)

[![GitHub Pages Deployment](https://img.shields.io/github/actions/workflow/status/aminblm/ai_systems_design_from_scratch/pages%2Fpages-build-deployment?label=docs%20deployment&logo=github&style=flat-square)](https://github.com/aminblm/ai_systems_design_from_scratch/actions)
[![System Modules Count](https://img.shields.io/badge/implemented%20systems-17%20Total-blueviolet?style=flat-square)](#matrix-of-technologies)
[![Architecture Framework](https://img.shields.io/badge/platform-GitHub%20Pages%20%2B%20Jekyll%20Pages%20%2B%20Python-orange?logo=jekyll&logoColor=white&style=flat-square)](https://github.com/aminblm/ai_systems_design_from_scratch)

<a href="https://www.producthunt.com/products/ai-systems-design-from-first-principles?embed=true&amp;utm_source=badge-featured&amp;utm_medium=badge&amp;utm_campaign=badge-ai-systems-design-from-first-principles" target="_blank" rel="noopener noreferrer"><img alt="AI Systems Design From First Principles - An implementation of AI Systems Design From First Principles | Product Hunt" width="250" height="54" src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=1173628&amp;theme=dark&amp;t=1781635927239"></a>

> *(Star⭐ our Repo)*

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>

---

A comprehensive, zero-dependency implementation of artificial intelligence components and enterprise systems design patterns, built completely from first principles.

**Amin Boulouma** — *Software Engineer*

---

## Repository Philosophy

> *Zero-Dependency Engineering* > — Core Philosophy

> **What I cannot create, I do not understand.** > — Richard Feynman

## Getting started 

To clone and use the repository, execute:

```
git clone https://github.com/aminblm/ai_systems_design_from_scratch.git
cd ai_systems_design_from_scratch
```

Run any core system directly from `src/`:

```
# Run the key-value cache store
python3 src/py_redis.py

# Run the task scheduler engine
python3 src/py_airflow.py

# Run the REST API backend framework
python3 src/py_REST_API.py
```

This repository sits at the exact intersection of deep education and production-grade implementation. The ultimate goal is to demystify the inner workings of complex enterprise software, cloud infrastructure, and machine learning ecosystems by rebuilding them atom by atom.

### The Zero-Dependency Mandate

To enforce genuine first-principles learning, this repository maintains a strict **zero-reliance policy on external libraries**.

* There is no `requirements.txt` or `pyproject.toml` containing third-party packages.
* The sole prerequisite is the native Python runtime.
* Higher-level systems (such as neural networks or orchestration engines) must strictly import and depend on the lower-level architectures built within this repository.

---

## What to Expect

* **Bridging the Complexity Gap:** Implementations balance fundamental simplicity with structural complexity, guiding you from beginner-level educational concepts to advanced systems design.
* **Full-Stack Systems Coverage:** Code components span across CI/CD mechanics, GoF design patterns, distributed databases, network load balancers, cloud primitives, and neural architectures.
* **Made for Builders:** Built specifically for hands-on software engineers, system architects, and AI scientists who learn best by writing raw code and breaking things.
* **Continuous Evolution:** This is a live, highly volatile work-in-progress framework. Systems are regularly refactored to achieve higher reliability, modularity, and throughput.

---

## Requirements

* **Runtime:** Python 3.14.5 (Standard Library Only)


---
## Technical Roadmap

### Code Base Standardization

* [ ] Implement a strict codebase-wide renaming convention to explicitly differentiate internal systems from upstream engines (e.g., refactoring `airflow` to `py_airflow`, `kafka` to `py_kafka`).
* [ ] Write a custom abstract syntax tree (AST) linter script to block accidental external imports.
* [ ] Integrate a pure-Python automated testing suite with unified coding guidelines.

### Reliability & Infrastructure Stress Testing

* [ ] Bind each complete system to a dedicated port and containerize via native process isolation techniques.
* [ ] Chain separate atomic technologies together to spin up end-to-end enterprise architectures.
* [ ] Develop an internal traffic engine to simulate heavy concurrency, network constraints, and system load.
* [ ] Inject custom chaos-engineering drivers to validate fault tolerance and state recovery during runtime failure.

### Community & Tooling Integration

* [ ] Enable packaging and execution testing via `uv` and `pip` exclusively for localized stress tests.
* [ ] Transition the project layout into an accessible prototyping framework for rapid offline infrastructure emulation.
* [ ] Compose comprehensive technical tutorials, architecture breakdowns, and system walkthroughs.

---

## Matrix of Technologies

Here is the updated, comprehensive list of all **71 distinct technologies, tools, and concepts** explicitly called out in your repository roadmap.

They are organized by operational domain so that you can easily copy and paste this block directly into your `README.md` or architectural planning documents.

---

### Complete Technology Implementation Registry

#### 1. Core Artificial Intelligence & Machine Learning

* [ ] **PyTorch** (Custom tensor structures and automatic differentiation tracking)
* [ ] **Tensorflow** (Alternative computation graph and execution engine)
* [ ] **Numpy** (Pure Python multi-dimensional array structures and matrix math routines)
* [ ] **Pandas** (DataFrames, Series, and structured data-manipulation mechanics)
* [ ] **Ollama** (Local LLM protocol orchestration and serving architecture)
* [ ] **Meta’s Llama** (Open-weights inference parser and layer-by-layer execution engine)
* [ ] **ChatGPT** (Upstream LLM API integration and chat state wrapper)
* [ ] **Hugging Face** (Model weight downloader and repository abstraction layer)
* [ ] **LangChain** (Prompt templates, custom tool integration, and chain-of-thought routing)
* [ ] **Vector Databases** (Embedding indexing algorithms such as Cosine Similarity and HNSW)
* [ ] **Recommender system** (Matrix factorization and collaborative filtering pipelines)
* [ ] **NLP** (Natural Language Processing tokenizers, stemmers, and bag-of-words text arrays)
* [ ] **Dedupe** (Record linkage, deduplication algorithms, and entity resolution)
* [ ] **Machine Learning** (Classic supervised/unsupervised algorithms from scratch)
* [ ] **NVIDIA’s AI/ML platforms** (Simulated compute abstractions modeling GPU optimization)
* [ ] **GCP AI Platform** (Managed machine learning model deployment simulation)
* [ ] **Models** (Unified base class interfaces for serving, training, and running model weights)

#### 2. Compute, Virtualization & Container Infrastructure

* [x] [**Docker Engine**](src/py_container_manager.py) (Core container manager daemon using process namespace isolation primitives)
* [x] [**Docker Client**](src/py_container_manager_CLI_client.py) (Command-line interface client to interact with your native Docker Engine)
* [ ] **Kubernetes** (Container orchestration node management, pod allocation, and state loops)
* [ ] **AKS** (Azure Kubernetes Service cloud wrapper orchestration)
* [ ] **EC2** (Elastic Compute Cloud virtual instance simulator with CPU allocation limits)
* [ ] **Lambda** (Serverless ephemeral function runner with event triggers)
* [ ] **Operating system** (Low-level task handling, file locks, and process scheduling)
* [ ] **GPU** (Emulated graphic processing unit thread allocation matrices)

#### 3. Core Networking, API & Web Architecture

* [x] [**Socket server**](src/py_socket_server.py) (Low-level TCP/IP listening, socket binding, and socket multiplexing)
* [x] [**Socket client**](src/py_socket_client.py) (Raw TCP connection handshake protocol and byte streamer)
* [x] [**Load Balancer**](src/py_load_balancer.py) (Traffic distribution mechanics featuring Round-Robin and Least-Connections)
* [x] [**FastAPI / Flask / RESTFUL API**](src/py_REST_API.py) (Pure Python REST API routing framework with request/response body parsing)
* [x] [**Postman / RESTFUL API Client**](src/py_REST_API_CLI_client.py) (Command-line REST API interface and endpoints stress-testing client)
* [x] [**Angular / React / Vue.js / Frontend**](src/py_frontend.py) (Component-based web client routing abstraction)
* [ ] **Node** (Server-side JavaScript runtime event execution engine simulation)
* [ ] **Npm** (Package manager installation validation tracker simulation)
* [ ] **API** (Standardized contract layer validation and schema constraints)
* [ ] **Google Chrome** (Virtual headless user-agent client agent for browsing simulation)

#### 4. Storage, Databases & Streaming

* [x] [**SQL Engine**](src/py_sql_engine.py) (Relational storage parser, indexing structures, and relational execution operators)
* [x] [**Redis**](src/py_redis.py) (In-memory key-value data structure store, caching layer, and pub/sub broker)
* [x] [**MongoDB**](src/py_mongo_db.py) (NoSQL BSON-like document engine, collection storage, and dynamic indexer)
* [x] [**ElasticSearch**](src/py_elasticsearch.py) (Inverted-index document retrieval system and text query engine)
* [ ] **Kafka** (Log-append streaming broker, distributed partition managers, and state logs)
* [ ] **S3** (Simple Storage Service bucket manager, object allocation, and metadata blobs)
* [ ] **Data lakes** (Unstructured multi-format data directories and partition layouts)
* [ ] **Databases** (Abstract state engine tracking transactions and ACID parameters)

#### 5. Data Orchestration, Ingestion & Pipelines

* [x] [**Airflow**](src/py_airflow.py) (Directed Acyclic Graph DAG job runner, scheduling loops, and task state tracking)
* [ ] **Pipelines** (Linear data transformers, staging maps, and stream extraction hooks)

#### 6. DevOps, Cloud Providers & Infrastructure as Code (IaC)

* [ ] **AWS** (Amazon Web Services API gateway and integrated resource layout ecosystem)
* [ ] **Azure** (Microsoft Azure cloud structural interface mapping)
* [ ] **GCP** (Google Cloud Platform workspace layout simulation)
* [ ] **LocalStack** (Local cloud stack mocking configuration layer)
* [ ] **Terraform** (Declarative configuration compiler mapping to your simulated cloud ecosystem)
* [ ] **Ansible** (Procedural configuration deployer mapping via terminal automation simulation)
* [ ] **CloudFormation** (AWS template resource deployment validation layout parser)
* [ ] **Jenkins** (Automated continuous-integration step executor and build scheduler)
* [x] [**Git server**](src/py_git_server.py) (Native Git packfile storage tracker, branch controllers, and remote hook scripts)
* [x] [**Git client**](src/py_git_client.py) (Native Git client)

#### 7. Observability, Monitoring & Cybersecurity

* [ ] **Prometheus** (Time-series metrics scraping engine and alert tracking arrays)
* [ ] **Grafana** (Metrics parser, dashboard generation charts, and numerical visualization grids)
* [ ] **New Relic** (Application Performance Monitoring telemetry tracker and hook agent)
* [ ] **AI + Cloud + DevOps + Cybersecurity** (Unified system boundary security configuration engine)

#### 8. Low-Level Core Runtimes & Engineering Utilities

* [ ] **Callables** (Dynamic functional interfaces and execution hooks)
* [ ] **Promises** (Asynchronous event loops, futures tracking, and unblocking resolution frameworks)
* [ ] **Design Patterns** (Unified implementation architecture featuring creational, structural, and behavioral patterns)
* [ ] **Documentation generator** (Source code AST parsing utility creating dynamic documentation pages)
* [ ] **Content generator** (Automated Markdown and project layout asset text provider)
* [ ] **Emailing server** (Simulated SMTP server tracking sent packets, relay connections, and standard text boxes)
* [ ] **Push Notification server** (Web-socket broadcast notification stream connection engine)
* [ ] **ServiceNow** (Enterprise ticketing management and tracking simulation dashboard)
* [ ] **VSCode** (Internal project text editing workspaces mapping configuration files)

### Other and Much more to come!

* [ ] **MkDocs** (static sites generators in Python)
* [x] [**Slug Generator**](src/py_slug_generator.py) (generate blop url slugs from blog titles)
* [x] [**Utility library**](src/utils.py) (utility library for reusable components)
* [ ] **LinkTree clone** (web links in one webpage)
* [ ] **Circle AI** (An AI partner that builds, runs, and grows your digital business with you)
* [ ] **Technologies in Job Descriptions** (Source for technologies from Job Descriptions)
* [x] **Jekyll**
* [ ] **BIOS**
* [x] **Markdown to HTML parser**
* [x] **YAML parser**
* [ ] **Virtual Environment**
* [ ] **Python To Markdown Generator**
* [ ] **Python To Markdown To HTML Generator**
* [ ] **Server on change listener**
* [ ] **Blog Posts Metas Appender** Append Blog posts with MEta and SEO data dynamically and automatically
* [ ] **Media Generator** Photo, video, gif 
* [ ] **Media converter** 
* [ ] **AST**
* [ ] **VS Code Extension**
* [ ] **Anything LLM**
* [ ] **AI Agents**
* [ ] **MAS Multi-Agent Systems**
* [ ] **Chain of thoughts**
* [ ] **Drug Discovery**
* [ ] **TDD / DDD**
* [ ] **Pip package manager**
* [ ] **Local LLM Model**
* [ ] **Blog Scrapper**
* [ ] **Landing Page Builder**
* [ ] **Roadmap builder**
* [ ] **CV Builder**
* [ ] **Scrapy**
* [ ] **LinkedIn Application Bot**
* [ ] **Diagram Generator**
* [ ] **Regex**
* [ ] **ServiceNow**
* [ ] **Odoo**
* [ ] **Async**
* [ ] **Concurrency**
* [ ] **Recursivity**
* [ ] **Wordpress**

### Possible evolutions of this repository

- Lightweight zero-dependency all-in-one infrastructure for rapid prototyping and validating systems before scale.
- Sandbox prototyping and local development

---

### Integration Architecture Checklists

* [ ] Ensure all components strictly rely on `ai_systems_design_from_scratch` dependencies.
* [ ] Prepend the `py_` namespace prefix across all relevant directories during implementation (e.g., `py_redis`, `py_kafka`, `py_tensorflow`).

---

## Contributing

Contributions are vital to pushing this framework toward absolute completeness. You can participate through the following avenues:

1. **Feature Proposals:** File an issue detailing an architectural component or cloud primitive you want to see built from scratch.
2. **Code Submissions:** Open a pull request containing optimization tweaks, behavioral alignment with target systems, or a new standard library implementation block.
3. **Architecture Reviews:** Audit existing components for edge-case errors, code readability problems, or violations of the zero-dependency rule.

<a href="https://linktr.ee/aminboulouma" 
   target="_blank" 
   rel="noopener noreferrer" 
   class="btn-primary" 
   style="display: inline-block; padding: 0.75rem 1.5rem; background-color: #000000; color: #ffffff; text-decoration: none; font-weight: bold; border-radius: 4px; transition: background-color 0.2s ease;">
   Connect with Amin Boulouma Official
</a>