# ROADMAP.md – code‑explorer  

*Version: 0.1 – Last updated 2026‑06‑20*  

---  

## 📌 Product Vision  

**code‑explorer** empowers developers to *navigate, understand, and modify* large, complex codebases faster. By combining a high‑performance code index with AI‑driven, personalized explanations, developers receive instant insights—right where they need them—without leaving their workflow.

---  

## 🎯 MVP (Minimum Viable Product) – **Launch‑Ready**  

| # | Feature | Description | MVP‑Critical* |
|---|---------|-------------|---------------|
| 1 | **Code Indexer & Search Engine** | Fast, incremental indexing of a single Git repository (supports Java, Python, C/C++, TypeScript). Full‑text + symbol‑aware search. | ✅ |
| 2 | **AI Query Engine** | Leverages **vLLM** for low‑latency inference; uses **SGLang** for structured generation of explanations (e.g., “What does this function do?”). | ✅ |
| 3 | **Web UI (Single‑Page)** | Minimal UI: file tree, code viewer with line‑highlight, query input, and AI‑generated answer pane. | ✅ |
| 4 | **Authentication & RBAC** | Simple OAuth2 (GitHub) login + role‑based read/write permissions per repository. | ✅ |
| 5 | **Basic CI/CD Integration** | Auto‑re‑index on push to default branch; webhook listener for GitHub/GitLab. | ✅ |
| 6 | **Performance & Scalability Benchmarks** | Target ≤ 200 ms latency for 10 k‑line query; support up to 5 concurrent users on a single node. | ✅ |
| 7 | **Observability** | Prometheus metrics + Grafana dashboards for indexing latency, query latency, error rates. | ✅ |
| 8 | **Documentation & Quick‑Start Guide** | README, API spec (OpenAPI), and a “Getting Started” video. | ✅ |

\* **MVP‑Critical** = must be shipped for launch; any missing item postpones go‑to‑market.

---  

## 🚀 Phase 1 – **v1.0** (Quarter 3 2026 → Quarter 4 2026)  

### Theme: *Collaboration & Multi‑Repo Mastery*  

| Milestone | Target Date | Key Deliverables |
|-----------|-------------|------------------|
| **Multi‑Repo Support** | 2026‑09‑15 | Index & query across multiple repositories; cross‑repo symbol resolution. |
| **Context‑Aware Explanations** | 2026‑10‑01 | Use **SGLang** to generate explanations that reference surrounding call‑graph, recent commits, and issue tickets. |
| **IDE Plug‑in (VS Code)** | 2026‑10‑20 | Inline “Ask AI” command, hover tooltips, and code‑action suggestions. |
| **Change‑Impact Analyzer** | 2026‑11‑10 | Show which files/functions are affected by a PR; AI‑generated risk summary. |
| **Collaboration Workspace** | 2026‑11‑30 | Shared query history, annotations, and team‑wide knowledge base. |
| **Enterprise Auth (SAML/OIDC)** | 2026‑12‑15 | Enterprise‑grade SSO integration & audit logging. |
| **Beta Release & Feedback Loop** | 2026‑12‑31 | Closed‑beta with 5 strategic partners; collect NPS & usage metrics. |

### Success Metrics (v1)

- ≥ 80 % of beta users report “faster code comprehension” (NPS ≥ +30).  
- Average query latency ≤ 150 ms for multi‑repo queries.  
- ≥ 90 % of indexed repositories refreshed within 5 min of push.  

---  

## 🌟 Phase 2 – **v2.0** (Quarter 1 2027 → Quarter 2 2027)  

### Theme: *Enterprise‑grade Intelligence & Extensibility*  

| Milestone | Target Date | Key Deliverables |
|-----------|-------------|------------------|
| **Custom Model Fine‑Tuning** | 2027‑02‑01 | UI to upload organization‑specific code‑base data; automated fine‑tuning using **auto** & **instr‑resp** datasets. |
| **Real‑Time Code Assistant** | 2027‑02‑28 | Inline suggestions while typing (autocomplete, refactor hints) powered by low‑latency vLLM. |
| **Offline / Edge Deployment** | 2027‑03‑15 | Docker‑compose & Helm charts for on‑prem deployment; encrypted local index. |
| **Advanced Analytics Dashboard** | 2027‑04‑01 | Heat‑maps of knowledge gaps, query trends, and code‑ownership insights. |
| **Plug‑in Marketplace** | 2027‑04‑20 | SDK for third‑party extensions (e.g., security scanners, test‑case generators). |
| **Compliance & Security Audits** | 2027‑05‑10 | SOC 2 Type II readiness, data‑retention policies, GDPR/CCPA controls. |
