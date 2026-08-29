# Governance, Human Oversight & RACI

This document applies across all three use cases in this repo. Each use-case PRD links back here instead of repeating this content.

## 9-Step Regulatory AI Agent Readiness Framework

Every proposed GenAI/agentic use case in this portfolio is assessed against these steps before being considered "ready":

1. **Identify the Use Case** — define exactly what the agent will do, and just as importantly, what it will *not* do.
2. **Define Context of Use** — determine how the output will be used, and who will rely on it downstream.
3. **Classify the Risk** — low / medium / high, based on potential business and customer impact if the agent is wrong.
4. **Assess Data Adoption** — determine whether the data involved is confidential, personal, proprietary, or commercially sensitive.
5. **Establish Human Oversight** — specify who must review and approve agent-generated outputs, and under what conditions the agent may act autonomously vs. must escalate.
6. **Validate Outputs** — define fact-checking, source verification, and quality-assessment procedures for agent output.
7. **Document AI Use** — maintain records of the tool, purpose, inputs, outputs, reviewer, and decision for every material agent action.
8. **Monitor Performance** — periodically evaluate accuracy, reliability, security, and business impact post-deployment.
9. **Review and Update** — reassess the use case as technology, business processes, data, and risk profile change.

## Oversight Pointers Applied to Every Agent

- **Data quality & governance** — no agent acts on stale, duplicate, or unvalidated source data; data freshness SLAs are defined per use case.
- **AI governance** — model choice, prompt versions, and guardrail logic are version-controlled and reviewable by a governance owner, not just the engineering team.
- **Cybersecurity** — agents operate with least-privilege access to inventory/ERP systems; no agent has standing write access without a human-approved action.
- **Human oversight** — every use case defines an explicit autonomy boundary (see each PRD's "Human-in-the-Loop" section) — what the agent can do unsupervised vs. what requires sign-off.
- **Output verification** — agent recommendations are checked against a simple, explainable business rule before being surfaced (e.g., "does this reorder quantity fall within X% of historical order size") — not just trusted because a model produced them.
- **Documentation & auditability** — every agent action that changes real-world state (a reorder trigger, a markdown, an allocation shift) is logged with the inputs, the agent's reasoning summary, the reviewer, and the outcome.
- **Company internal audit & compliance** — agent decision logs are structured so an internal auditor can reconstruct "why did the agent do this" without needing to read source code.

## RACI — Dark-Store Stockout Agent (Flagship)

| Activity | Category Manager | Store Ops Lead | Data/ML Engineer | AI Governance Owner | Supply Chain Planner |
|---|---|---|---|---|---|
| Define SKU scope & thresholds | A | C | C | I | R |
| Approve reorder trigger logic | A | I | R | C | C |
| Review flagged low-confidence predictions | C | R | I | I | A |
| Sign off on agent going from "recommend" to "auto-trigger" for a SKU tier | A | C | C | R | C |
| Monthly accuracy/drift review | I | I | R | A | C |
| Incident review (agent caused stockout or over-order) | C | R | C | A | C |

*R = Responsible, A = Accountable, C = Consulted, I = Informed. The same roles map onto the two one-pager use cases with only the "Category Manager" role swapped for the relevant store/assortment or B2B account owner — not re-tabulated per use case.*

## Data Sensitivity Note

All input data described in this portfolio (12–18 months of SKU/store/date-level sales history, current stock levels, supplier lead times) is treated as **commercially sensitive** even though it is not personal data — RACI and access controls apply accordingly.
