# Business Model Canvas – **code‑explorer**  
*AI‑powered code navigation & insight platform for developers working with large, complex codebases.*

| **Key Partners** | **Key Activities** | **Key Resources** |
|------------------|--------------------|-------------------|
| • Large‑scale open‑source projects (e.g., Linux, LLVM, Kubernetes) – source of diverse codebases for training & demo | • Build & maintain the AI inference pipeline (vLLM, SGLang) | • Proprietary model fine‑tuned on 22 M+ code‑related pairs (auto, instr‑resp, messages, query‑resp) |
| • Cloud providers (AWS, GCP, Azure) – GPU/TPU compute & storage | • Continuous data ingestion & pair generation (≈144 M new pairs / week) | • Axentx Knowledge Graph (pgvector) for context & retrieval |
| • IDE vendors (JetBrains, Microsoft VS Code) – integration partners | • Develop and ship IDE plugins & web UI | • Production inference engine (vLLM) for low‑latency responses |
| • Enterprise security & compliance auditors | • Run validation studies (pain‑point & willingness‑to‑pay) | • Documentation & support team |
| • Community contributors (open‑source contributors, university labs) | • Conduct user research & iterate on UX | • Licensing & legal compliance frameworks |

| **Value Propositions** | **Customer Segments** |
|------------------------|-----------------------|
| • **Instant, contextual explanations** of any symbol, function, or flow in a massive codebase, powered by a fine‑tuned LLM. | • **Enterprise dev teams** (FinTech, SaaS, embedded) that maintain monolithic or micro‑service repositories >10 M LOC. |
| • **Personalized navigation** – “jump to definition”, “show call graph”, “explain algorithm” in natural language. | • **Individual developers & freelancers** tackling unfamiliar open‑source projects. |
| • **Reduced onboarding time** – new hires become productive 30‑40 % faster. | • **Tooling vendors** (IDE platforms, code review SaaS) seeking AI augmentation. |
| • **Secure, on‑premise deployment** for regulated industries (healthcare, finance). | • **Education & boot‑camps** needing interactive code walkthroughs. |
| • **Continuous learning** – the system improves as more code‑pair data is harvested. | |

| **Channels** | **Revenue Streams** |
|--------------|---------------------|
| • Direct sales & enterprise contracts (SaaS + on‑prem). | • **Subscription SaaS** – tiered per‑seat pricing (Developer, Team, Enterprise). |
| • Marketplace listings in JetBrains Plugin Repository & VS Code Marketplace. | • **On‑premise licensing** – perpetual license + annual support. |
| • API access for tooling partners (pay‑per‑call). | • **Professional services** – custom integration, training, and fine‑tuning for proprietary code. |
| • Developer community webinars, open‑source demos, hackathon sponsorships. | • **Data‑augmentation services** – selling curated code‑pair datasets to AI research labs. |
| • Content marketing (blog, case studies, whitepapers). | • **Referral/partner commissions** from IDE vendors. |

| **Cost Structure** |
|--------------------|
| • **Compute** – GPU/TPU clusters for inference (vLLM) and continuous fine‑tuning (≈ $0.12 / GPU‑hour). |
| • **Data acquisition & licensing** – maintaining the 22 M+ pair corpus, compliance checks. |
| • **Engineering salaries** – AI/ML scientists, backend, frontend, DevOps. |
| • **Cloud storage & bandwidth** – codebase snapshots, vector index (pgvector). |
| • **Sales & marketing** – enterprise outreach, marketplace fees. |
| • **Legal & security** – audits for on‑premise deployments, GDPR/CCPA compliance. |
| • **Support & success** – tier‑1/2 support staff, SLA tooling. |

---  

*Prepared by the Senior Product/Engineering Lead, Axentx – 2026‑06‑20*
