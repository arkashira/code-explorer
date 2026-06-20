# PRD – Code‑Explorer
**Product:** Code‑Explorer  
**Owner:** Senior Product/Engineering Lead – Axentx  
**Date:** 2026‑06‑20  
**Version:** 1.0  

---

## 1. Problem Statement  

Developers spending time in large, unfamiliar codebases face three recurring pain points:

| Pain Point | Impact | Why Existing Tools Fall Short |
|------------|--------|------------------------------|
| **Context‑switching & mental load** | ↑ development time by 30‑45 % per feature | IDE “go‑to‑definition” shows only syntax; no higher‑level rationale. |
| **Out‑of‑date or missing documentation** | ↑ bug rate, ↑ on‑call fatigue | Docs are static, quickly become stale, and rarely explain *why* a piece exists. |
| **Onboarding bottleneck** | New hires need weeks to become productive | Knowledge is siloed in senior engineers; manual walkthroughs are costly. |

**Result:** Slower delivery, higher defect rates, and increased engineering cost.

---

## 2. Target Users  

| Persona | Primary Need | Frequency of Use |
|---------|--------------|------------------|
| **Mid‑senior backend engineer** (5‑8 y) | Quickly understand a function/class they never wrote | Daily – multiple times per ticket |
| **New hire / junior engineer** (0‑2 y) | Guided walkthrough of critical modules | 3‑5 times per week during onboarding |
| **Tech lead / architect** | Verify design intent across the repo & surface hidden coupling | Weekly – during design reviews |
| **DevOps / SRE** | Trace runtime errors to source logic without deep code dive | As needed – on incident response |

---

## 3. Goals & Success Metrics  

| Goal | Metric | Target (12 mo) |
|------|--------|----------------|
| **Reduce time‑to‑understand** | Avg. minutes to answer “What does X do?” (survey) | ↓ 50 % (from 12 min → 6 min) |
| **Increase onboarding velocity** | New‑hire PR acceptance time | ↓ 30 % (from 4 d → 2.8 d) |
| **Lower defect leakage** | Post‑release bugs traced to misunderstood code | ↓ 20 % |
| **Adoption** | Active daily users (DAU) / total engineers | ≥ 40 % |
| **Revenue validation** | Paid‑pilot conversion (enterprise teams) | 3 × pilot → paid contract within 6 mo |

---

## 4. Key Features (Prioritized)

| Priority | Feature | Description | Acceptance Criteria |
|----------|---------|-------------|----------------------|
| **P1** | **AI‑driven code explanation engine** | Generates concise, context‑aware natural‑language explanations for any symbol (function, class, macro) in the repo. | • Input: file path + line range → output ≤ 3 sentences.<br>• Accuracy ≥ 85 % vs. senior‑engineer review.<br>• Latency ≤ 800 ms for repos ≤ 5 M LOC. |
| **P1** | **Interactive “Ask‑Me‑Anything” chat** | Inline chat widget (VS Code & JetBrains plugins) that lets developers ask follow‑up questions (“Why is this guard needed?”). | • Conversation persists per file session.<br>• Model retains context across ≥ 5 turns.<br>• No‑hallucination guard: fallback to “I’m not sure” when confidence < 70 %. |
| **P2** | **Cross‑reference graph view** | Visual map of call‑graph / dependency edges highlighted with AI‑generated rationale nodes. | • Click a node → open explanation panel.<br>• Exportable as SVG/JSON.<br>• Works for both monorepo and multi‑repo setups. |
| **P2** | **Documentation sync & suggestion** | Detects mismatches between code comments and AI‑generated intent; proposes PR‑ready doc updates. | • Shows diff with confidence score.<br>• Auto‑generate PR draft on approval. |
| **P3** | **Enterprise policy & data isolation** | On‑prem deployment mode with RBAC, audit logs, and ability to run LLM inference on isolated hardware. | • Meets ISO‑27001 & SOC‑2 baseline.<br>• No outbound network traffic in on‑prem mode. |
| **P3** | **Metrics dashboard** | Team‑level analytics (queries per repo, average explanation time, knowledge‑gap heatmap). | • Exportable CSV.<br>• Configurable retention (30 d‑1 y). |

---

## 5. Scope  

### In‑Scope (MVP – 6 months)
- AI explanation engine powered by **vLLM** (GPU‑accelerated inference) using a fine‑tuned LLaMA‑2‑13B model.
- VS Code extension with hover‑tooltip and chat panel.
- Basic cross‑reference graph for a single repository.
- Documentation suggestion workflow (read‑only preview, manual PR creation).
- Core telemetry (usage counts, latency, error rates).

### Out‑of‑Scope (Post‑MVP)
- Full JetBrains plugin suite (deferred to Q4 2027).
- Multi‑repo federation UI (initially single‑repo focus).
- Advanced “code‑rewrite” suggestions (only explanations for now).
- Custom model training UI (model updates handled by Ops team).

---

## 6. Assumptions & Dependencies  

| Assumption | Rationale |
|------------|-----------|
| Access to the **auto** and **instr‑resp** datasets for fine‑tuning. | Provides code‑question pairs aligned with our domain. |
| vLLM inference can be served at ≤ 800 ms for 5 M LOC repos on our current GPU fleet. | Benchmarks from internal tests (2026‑05). |
| Developers will install the VS Code extension voluntarily during pilot. | Low friction; VS Code market share > 65 % among target personas. |
| Security review will approve on‑prem container images within 4 weeks. | Required for enterprise customers. |

**Dependencies**
- **vLLM** repo (vllm‑project/vllm) – production inference engine.
- **SGLang** for structured generation of explanation payloads.
- Internal CI/CD pipeline for model fine‑tuning (uses `arkashira/surrogate-1-harvest`).
- Telemetry stack (OpenTelemetry + Grafana) already provisioned.

---

## 7. Risks & Mitigations  

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Hallucination / inaccurate explanations** | Reduces trust, slows adoption | Implement confidence scoring; fallback to “I’m not sure”; human‑in‑the‑loop review for first 10 k queries. |
| **Performance degradation on very large repos** | Poor UX → churn | Auto‑sharding of index; cache frequently accessed symbols; fallback to static doc if latency > 2 s. |
| **Data privacy concerns for on‑prem customers** | Block enterprise sales | Provide fully isolated Docker image; support customer‑provided model weights. |
| **Model drift as code patterns evolve** | Degraded accuracy over time | Quarterly re‑fine‑tune using newly collected `messages` dataset; automated CI test suite with regression checks. |
| **Extension compatibility across OS versions** | Installation friction | CI matrix testing on Windows, macOS, Linux; publish via VS Code Marketplace with auto‑updates. |

---

## 8. Milestones & Timeline  

| Milestone | Deliverable | Owner | Target Date |
|-----------|-------------|-------|-------------|
| **M1 – Foundations** | vLLM inference service deployed; fine‑tuned model checkpoint | Infra / ML | 2026‑07‑15 |
| **M2 – VS Code Prototype** | Hover tooltip & basic chat UI (beta) | Front‑end | 2026‑08‑30 |
| **M3 – Cross‑Reference Graph** | Interactive graph view for single repo | Backend | 2026‑09‑25 |
| **M4 – Documentation Sync** | Diff generation & PR draft workflow | Backend | 2026‑10‑20 |
| **M5 – Pilot Launch** | 5 internal teams + 2 external beta customers | PM / Sales | 2026‑11‑15 |
| **M6 – Enterprise Hardening** | On‑prem container, RBAC, audit logs | Security / Ops | 2026‑12‑31 |
| **M7 – GA Release** | Public VS Code extension, telemetry dashboard | All | 2027‑02‑15 |

---

## 9. Acceptance Test Checklist  

- [ ] AI explanation returns ≤ 3 sentences with ≥ 85 % factual accuracy (validated by senior engineers).  
- [ ] Chat latency ≤ 800 ms; fallback works when confidence < 70 %.  
- [ ] Graph view loads for repos up to 5 M LOC within 2 s.  
- [ ] Documentation suggestion creates a clean PR diff without breaking CI.  
- [ ] Telemetry records: `explanations_requested`, `avg_latency_ms`, `error_rate`.  
- [ ] Security scan passes for on‑prem image (no external network calls).  

---

## 10. Open Questions  

1. **Model size vs. latency trade‑off** – Should we offer a 7B “fast” variant for low‑resource environments?  
2. **Pricing model** – Seat‑based vs. usage‑based for enterprise?  
3. **Support for non‑Git repos** (e.g., Perforce) – future roadmap consideration.  

---

*Prepared by the Code‑Explorer product team. All stakeholders are invited to review and provide feedback by 2026‑06‑30.*
