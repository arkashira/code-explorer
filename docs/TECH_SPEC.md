# TECH_SPEC.md

## Project Overview
**code‑explorer** is an AI‑powered code‑base navigation and understanding tool. It enables developers to query large, complex repositories and receive personalized, context‑aware explanations, visualizations, and actionable insights. The system combines static analysis, vector‑based code embeddings, and large language model (LLM) inference to surface relevant code fragments, generate natural‑language summaries, and suggest refactorings or usage patterns.

The product is built on Axentx’s core infrastructure:
- **vLLM** for high‑throughput LLM inference  
- **SGLang** for structured generation of explanations and code snippets  
- **Axentx BRAIN (pgvector)** for storing and retrieving code embeddings  

The specification below details the architecture, components, data model, APIs, tech stack, dependencies, and deployment model required to ship a production‑ready version of **code‑explorer**.

---

## Table of Contents
1. [Architecture Overview](#architecture-overview)  
2. [Core Components](#core-components)  
3. [Data Model](#data-model)  
4. [Key APIs & Interfaces](#key-apis--interfaces)  
5. [Tech Stack & Dependencies](#tech-stack--dependencies)  
6. [Deployment & Ops](#deployment--ops)  
7. [Security & Compliance](#security--compliance)  
8. [Observability & Monitoring](#observability--monitoring)  
9. [Scalability & Performance Targets](#scalability--performance-targets)  
10. [Future Extensions](#future-extensions)  

---

## Architecture Overview
```
+-------------------+          +-------------------+          +-------------------+
|   Client (Web /   |  HTTPS   |   API Gateway /   |  gRPC/   |   Inference       |
|   VSCode Plugin) |<-------->|   Auth Service    |<-------->|   Service (vLLM) |
+-------------------+          +-------------------+          +-------------------+
          |                               |                           |
          |                               |                           |
          v                               v                           v
+-------------------+          +-------------------+          +-------------------+
|   Query Router    |<-------> |   Embedding Store |<-------> |   LLM (SGLang)    |
|   (FastAPI)       |          |   (Postgres +    |          |   (vLLM + SGLang) |
|                   |          |    pgvector)     |          +-------------------+
+-------------------+          +-------------------+
          |
          v
+-------------------+
|   Code Indexer    |
|   (Background)   |
+-------------------+
```

* **Client** – Web UI (React) and VS Code extension. Sends user queries and receives streamed responses.
* **API Gateway** – Handles authentication (OAuth2/JWT), rate‑limiting, and request routing.
* **Query Router** – FastAPI service that orchestrates:
  * Retrieval of relevant code embeddings from the vector store.
  * Construction of LLM prompts (structured via SGLang).
  * Streaming of LLM responses back to the client.
* **Embedding Store** – PostgreSQL with pgvector extension. Stores per‑file/function embeddings, metadata, and versioning.
* **Inference Service** – vLLM deployment (GPU‑accelerated) serving the chosen LLM (e.g., Llama‑3‑8B‑Instruct). SGLang wraps the model to enforce structured output schemas.
* **Code Indexer** – Background workers (Celery + Redis) that:
  * Parse repositories (tree‑sitter, clang‑tools, etc.).
  * Generate embeddings using a dedicated embedding model (e.g., sentence‑transformers).
  * Update the vector store incrementally on git pushes.

All services are containerized (Docker) and orchestrated via Kubernetes (Helm charts provided).

---

## Core Components

| Component | Responsibility | Language / Runtime | Key Libraries |
|-----------|----------------|--------------------|----------------|
| **Client UI** | Interactive query editor, result rendering, code navigation | TypeScript (React) | Redux, Material‑UI, Monaco editor |
| **VSCode Extension** | In‑IDE query shortcut, inline annotations | TypeScript | VSCode API |
| **API Gateway** | Auth, rate‑limit, TLS termination | Go (Gin) | OIDC, Redis‑based token bucket |
| **Query Router** | Orchestrates retrieval + generation, streaming | Python 3.11 (FastAPI) | httpx, asyncpg, pgvector, sglang |
| **Embedding Store** | Persistent vector DB + metadata | PostgreSQL 15 + pgvector | SQLAlchemy |
| **Code Indexer** | Repo parsing → embedding pipeline | Python (Celery) | tree‑sitter, clang‑python, sentence‑transformers |
| **Inference Service** | LLM inference (high throughput) | Python (vLLM) | vLLM, torch, transformers |
| **SGLang Wrapper** | Structured output schema enforcement | Python | sglang |
| **Observability** | Tracing, metrics, logs | Go / Python | OpenTelemetry, Prometheus, Loki |

---

## Data Model

### 1. Code Entity
```sql
CREATE TABLE code_entities (
    id            BIGSERIAL PRIMARY KEY,
    repo_id       UUID NOT NULL,
    commit_hash   TEXT NOT NULL,
    path          TEXT NOT NULL,          -- relative file path
    start_line    INT NOT NULL,
    end_line      INT NOT NULL,
    language      TEXT NOT NULL,
    content_hash  TEXT NOT NULL,          -- SHA256 of the snippet
    embedding     VECTOR(1536) NOT NULL,  -- dimension matches embedding model
    metadata      JSONB,                  -- e.g., symbols, docstrings
    created_at    TIMESTAMPTZ DEFAULT now(),
    updated_at    TIMESTAMPTZ DEFAULT now()
);
```

### 2. Repository Metadata
```sql
CREATE TABLE repositories (
    id            UUID PRIMARY KEY,
    name          TEXT NOT NULL,
    remote_url    TEXT NOT NULL,
    default_branch TEXT NOT NULL,
    last_indexed  TIMESTAMPTZ,
    created_at    TIMESTAMPTZ DEFAULT now()
);
```

### 3. Query Log (for analytics & RLHF)
```sql
CREATE TABLE query_logs (
    id            BIGSERIAL PRIMARY KEY,
    user_id       UUID NOT NULL,
    repo_id       UUID,
    query_text    TEXT NOT NULL,
    response_text TEXT,
    latency_ms    INT,
    rating        SMALLINT,               -- optional user feedback 1‑5
    created_at    TIMESTAMPTZ DEFAULT now()
);
```

### 4. Prompt Templates (SGLang)
Stored as JSON in a separate table or config repo; versioned for A/B testing.

---

## Key APIs & Interfaces

### 1. Public REST API (client ↔ gateway)

| Method | Path | Auth | Description | Request Body | Response |
|--------|------|------|-------------|--------------|----------|
| POST | `/api/v1/query` | Bearer JWT | Submit a natural‑language query. Returns a streaming endpoint URL. | `{ "repo_id": "uuid", "query": "string", "options": { "max_tokens": 512 } }` | `202 Accepted` + `{ "stream_url": "/api/v1/stream/<id>" }` |
| GET | `/api/v1/stream/{id}` | Bearer JWT | Server‑Sent Events (SSE) stream of LLM response chunks. | – | `text/event-stream` |
| POST | `/api/v1/repo/{repo_id}/index` | Service‑to‑service token | Trigger re‑index of a repository (used by CI webhook). | – | `202 Accepted` |
| GET | `/api/v1/healthz` | – | Liveness/Readiness probe. | – | `{ "status":"ok" }` |

### 2. Internal gRPC (Query Router ↔ Inference Service)

```proto
service Inference {
  rpc Generate (GenerateRequest) returns (stream GenerateResponse);
}

message GenerateRequest {
  string prompt = 1;
  uint32 max_tokens = 2;
  map<string, string> metadata = 3; // repo, commit, etc.
}

message GenerateResponse {
  string text_chunk = 1;
  bool is_final = 2;
}
```

### 3. Embedding Retrieval (SQL via asyncpg)

```sql
SELECT id, path, start_line, end_line, embedding
FROM code_entities
WHERE embedding <=> $1::vector
ORDER BY embedding <=> $1::vector
LIMIT $2;
```
*`<=>` is pgvector’s cosine distance operator.*

### 4. VSCode Extension RPC (WebSocket)

- `query` → sends JSON `{repoId, query}`  
- `result` → receives streaming JSON `{chunk, isFinal}`  

---

## Tech Stack & Dependencies

| Layer | Technology | Version | Rationale |
|-------|-------------|---------|-----------|
| **Container Runtime** | Docker | 24.x | Standardized builds |
| **Orchestration** | Kubernetes | 1.28 | Autoscaling, self‑healing |
| **Helm** | 3.14 | Package management |
| **API Gateway** | Go (Gin) | 1.9 | Low‑latency, native TLS |
| **Web UI** | React 18 + TypeScript 5 | SPA | Rich interactive UI |
| **VSCode Extension** | TypeScript 5 | VSCode 1.88 API |
| **Backend** | Python 3.11 | FastAPI 0.109, asyncpg 0.29 |
| **LLM Inference** | vLLM 0.4.0 | GPU‑accelerated, supports tensor parallelism |
| **Structured Generation** | SGLang 0.2.1 | Guarantees JSON schema output |
| **Embedding Model** | sentence‑transformers/all‑mpnet‑base‑v2 | 768‑dim | Good trade‑off speed/quality |
| **Vector Store** | PostgreSQL 15 + pgvector 0.5 | Proven, ACID‑compliant |
| **Task Queue** | Celery 5.4 + Redis 7 | Scalable background jobs |
| **Observability** | OpenTelemetry SDK (Python/Go) | Prometheus + Grafana + Loki |
| **Auth** | Keycloak 24 (OIDC) | Centralized identity |
| **CI/CD** | GitHub Actions + Argo CD | Automated testing & deployment |

All third‑party libraries are vetted for compatible licenses (Apache‑2.0, MIT, BSD).

---

## Deployment & Operations

### 1. Helm Chart Structure
```
code-explorer/
├─ charts/
│  ├─ api-gateway/
│  ├─ query-router/
│  ├─ inference/
│  ├─ indexer/
│  └─ postgres/
├─ values.yaml
└─ templates/
```
* Each chart defines Deployment, Service, HorizontalPodAutoscaler, and ConfigMap for environment variables.

### 2. CI Pipeline
1. **Lint / TypeCheck** – ESLint (UI), mypy (Python), golangci‑lint (Go).  
2. **Unit Tests** – Jest (UI), pytest (Python), go test (gateway).  
3. **Integration Tests** – Docker‑compose environment with mock LLM.  
4. **Security Scan** – Trivy, Dependabot.  
5. **Build Images** – BuildKit, push to internal registry.  
6. **Helm Release** – Argo CD sync to `staging`; manual promotion to `prod`.

### 3. Autoscaling Policies
| Service | Metric | Target |
|---------|--------|--------|
| API Gateway | CPU | 70% |
| Query Router | Request latency (p95) | < 200 ms |
| Inference (vLLM) | GPU memory usage | 80% |
| Indexer Workers | Queue length | < 100 tasks |

### 4. Data Persistence
* PostgreSQL cluster (Patroni) with 3‑node replica set.  
* Daily backups to encrypted S3 bucket, retention 30 days.  
* Embedding vectors stored in pgvector column; periodic vacuum to reclaim space.

### 5. Secrets Management
* HashiCorp Vault for DB passwords, API keys, and JWT signing keys.  
* Kubernetes secrets populated via Vault Agent Injector.

---

## Security & Compliance

| Aspect | Implementation |
|--------|----------------|
| **Authentication** | OIDC via Keycloak; JWT signed with RS256. |
| **Authorization** | Scope‑based RBAC (read‑repo, query, admin). |
| **Transport Security** | All endpoints TLS 1.3; mTLS between internal services. |
| **Data Privacy** | Code snippets are stored only as hashed embeddings; raw source never persisted beyond indexing stage. |
| **Audit Logging** | All query requests logged with user ID, repo ID, timestamp. |
| **Compliance** | Licenses of all third‑party components are tracked; GDPR‑compliant data‑retention policies. |

---

## Observability & Monitoring

* **Metrics** – Prometheus exporters on each service (FastAPI, Go Gin, vLLM). Key metrics: request_rate, latency, GPU utilization, queue depth.  
* **Tracing** – OpenTelemetry traces propagated across HTTP/gRPC boundaries; view in Jaeger.  
* **Logging** – Structured JSON logs shipped to Loki; include request IDs for correlation.  
* **Alerting** – Grafana alerts on: API error rate > 1%, inference latency > 500 ms, DB replication lag > 5 s.  

---

## Scalability & Performance Targets

| Metric | Target (99th percentile) |
|--------|--------------------------|
| Query latency (router → LLM) | ≤ 350 ms |
| End‑to‑end response (including streaming) | ≤ 800 ms |
| Embedding retrieval time (top‑5 results) | ≤ 30 ms |
| Indexer throughput | ≥ 10 k files / hour per worker |
| Concurrent users | 5 000 active sessions with graceful degradation |

Horizontal scaling of the inference service and query router will meet load spikes. Vector store sharding can be introduced later if dataset exceeds 100 M embeddings.

---

## Future Extensions

1. **Multi‑repo cross‑search** – Unified index across organization‑wide repos.  
2. **Fine‑tuned domain LLM** – Train on internal code‑base to improve accuracy.  
3. **Interactive Refactoring** – Generate patches and submit PRs automatically.  
4. **Explainability UI** – Graph view of call‑graph and data‑flow highlighted per query.  
5. **Feedback Loop** – Use `query_logs.rating` to perform RLHF on the LLM.  

--- 

*Prepared by:*  
Senior Product/Engineering Lead – code‑explorer  
Axentx OS – Autonomous AI‑Workforce  

*Date:* 2026‑06‑20
