# REQUIREMENTS.md

## 1. Overview
**Product:** **code‑explorer**  
**Purpose:** Provide developers with an AI‑powered navigation and understanding experience for large, complex codebases. The tool indexes source code, enables fast semantic search, and generates personalized, context‑aware explanations, refactoring suggestions, and impact analyses directly within the developer’s workflow.

**Target Users:** Software engineers, technical leads, and DevOps staff who need to quickly comprehend unfamiliar or legacy code, perform impact assessments, and onboard new team members.

**Key Technologies (as per Axentx knowledge base):**
- **vLLM** – production‑grade inference engine for LLM serving.  
- **SGLang** – structured generation for deterministic, token‑level control.  
- **Axentx data assets** – `auto`, `instr‑resp`, `messages`, `query‑resp` datasets for fine‑tuning and prompt engineering.  

---

## 2. Scope
| In‑Scope | Out‑of‑Scope |
|----------|--------------|
| • Indexing of local and remote Git repositories (any language). | • Full IDE replacement (e.g., code editing, compilation). |
| • Semantic code search (keyword + vector similarity). | • Automated code generation beyond explanatory snippets. |
| • AI‑driven explanations, “what‑does‑this‑function‑do?” and impact analysis. | • Runtime profiling or performance benchmarking of the target code. |
| • VS Code and JetBrains plugin integrations (read‑only). | • Cloud‑hosted SaaS offering (product ships as self‑hosted). |
| • CLI for batch processing and CI integration. | • Support for binary‑only repositories (no source). |
| • Role‑based access control for multi‑user environments. | • Real‑time collaborative editing. |

---

## 3. Functional Requirements

| ID | Description |
|----|-------------|
| **FR‑1** | **Repository Ingestion** – The system shall accept a Git repository via (a) local path, (b) SSH/HTTPS URL, or (c) a pre‑zipped archive. It must clone (or unpack) the repo, resolve sub‑modules, and store a read‑only snapshot for indexing. |
| **FR‑2** | **Language Detection & Parsing** – Automatically detect supported languages (at minimum: Python, JavaScript/TypeScript, Java, C/C++, Go, Rust) and invoke the appropriate parser to build an abstract syntax tree (AST) for each file. |
| **FR‑3** | **Code Indexing** – Generate (a) lexical token indexes, (b) AST‑based symbol tables, and (c) dense vector embeddings (using the `auto` dataset‑derived model) for every source file, function, class, and comment block. Indexes must be persisted in a searchable store (e.g., SQLite + FAISS). |
| **FR‑4** | **Semantic Search API** – Expose a RESTful endpoint `POST /search` that accepts a natural‑language query and returns the top **N** (configurable) code snippets ranked by combined lexical + vector similarity, with source file path, line range, and a short relevance score. |
| **FR‑5** | **AI Explanation Service** – Given a code identifier (file + symbol) or a raw snippet, the system shall invoke the LLM (via vLLM) to produce: <br>• a concise description (≤ 2 sentences), <br>• a detailed walkthrough (≤ 200 words), <br>• identified dependencies & potential side‑effects. |
| **FR‑6** | **Impact Analysis** – For a selected function/method, generate a list of call‑graph downstream callers (up to configurable depth) and summarize the risk of modification (e.g., “high risk: modifies global state”). |
| **FR‑7** | **IDE Plugin Integration** – Provide a VS Code extension and a JetBrains plugin that: <br>• displays a side‑panel with search results, <br>• shows AI‑generated explanations inline (hover or command), <br>• allows “copy to clipboard” of generated text. |
| **FR‑8** | **CLI Interface** – Implement a command‑line tool `code-explorer` with sub‑commands: `index`, `search`, `explain`, `impact`, and `serve` (starts local API server). |
| **FR‑9** | **User Authentication & RBAC** – Support local users (username/password) and optional LDAP/OIDC. Permissions: `viewer`, `analyst`, `admin`. Only `admin` can trigger re‑indexing. |
| **FR‑10** | **Audit Logging** – Record every search, explanation, and impact request with timestamp, user ID, query text, and result hash. Logs must be write‑once and rotatable. |
| **FR‑11** | **Configuration Management** – All tunable parameters (model path, index directory, max concurrent requests, etc.) shall be defined in a single YAML file (`config.yaml`) and reloadable without restarting the service. |
| **FR‑12** | **Model Update Pipeline** – Provide a script `scripts/update_model.sh` that fine‑t
