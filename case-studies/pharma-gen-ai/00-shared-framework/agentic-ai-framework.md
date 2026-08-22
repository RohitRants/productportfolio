# Agentic AI Governance Framework — Pharma Business Development

This framework applies to all six GenAI use cases in this repo. It exists to answer one question for every use case, before any prompt gets written: **what is the AI allowed to decide on its own, and what must a human decide instead?**

It's built around three layers: a **9-step readiness process** (what to check before and after deploying any agent), **6 readiness dimensions** (what "ready" actually means, organizationally), and a set of **agent role definitions with sample instructions** (what the agents actually do, day to day).

---

## Layer 1 — The 9-Step Regulatory AI Agent Readiness Process

Every proposed use case in this repo is run through these nine steps before it's considered scoped:

| Step | Question it answers | Owner |
|---|---|---|
| 1. Identify the Use Case | What exactly will GenAI do — and, as importantly, what won't it do? | Product (AI PM) |
| 2. Define Context of Use | Who relies on the output, and for what kind of decision? | Product + Business stakeholder |
| 3. Classify the Risk | Low / medium / high, based on potential business, scientific, or regulatory impact | Product + Regulatory/Compliance |
| 4. Assess Data Adoption | Does the input data contain confidential, personal, proprietary, regulated, or commercially sensitive information? | Data Governance |
| 5. Establish Human Oversight | Who must review and approve outputs before they're acted on? | Business stakeholder (named role, not "someone") |
| 6. Validate Outputs | What's the fact-checking, source-verification, and quality bar? | Reviewer + Regulatory/Compliance |
| 7. Document AI Use | Tool, purpose, inputs, outputs, reviewer, decision — logged, not tribal knowledge | Product + AI Governance |
| 8. Monitor Performance | Accuracy, reliability, security, business impact — checked on a cadence, not just at launch | AI Governance |
| 9. Review and Update | Reassess as regulation, technology, or business process changes | Product + AI Governance |

This is consistent with the direction of current pharma AI regulatory thinking — FDA's emphasis on *context of use* and *credibility*, and EMA's emphasis on AI being safe, effective, transparent, and trustworthy throughout the medicinal-product lifecycle. Every use case folder in this repo states, up front, which risk tier it lands in and why.

---

## Layer 2 — Readiness Dimensions

A use case isn't "ready" just because the model works. It's ready when all six of these are true:

- **Regulatory & Compliance Readiness** — applicable regulations understood, AI policy defined, risk classified, compliance ownership assigned, regulatory change monitored
- **Data Governance Readiness** — data classified, confidentiality controls in place, privacy respected, data quality checked, access controlled, retention/traceability defined
- **AI Governance Readiness** — only approved tools used, model ownership assigned, use case registered centrally, risk assessed, human oversight defined, incident process exists
- **Technical Readiness** — infrastructure, cybersecurity, system integration, access management, output monitoring, model performance monitoring
- **Human & Organizational Readiness** — AI literacy, training, cross-functional governance, accountability, change management, leadership support
- **Process Readiness** — SOPs, output verification steps, documentation, audit trails, escalation paths, periodic review

Each use case one-pager references which of these it leans on hardest — due diligence, for example, lives and dies on Data Governance Readiness; strategic analysis leans hardest on Process Readiness (because the "output" is a recommendation, not a fact).

---

## Layer 3 — Agent Roles & Sample Instructions

Rather than one monolithic "AI," every use case is decomposed into narrow agents with a defined job, defined inputs, and a defined human checkpoint. Three roles recur across all six use cases:

### Research / Retrieval Agent
Gathers and synthesizes information from approved external and internal sources. Never makes a recommendation — only surfaces findings with sources attached.

```
You are a Research Agent supporting pharma business development analysis.

Your job:
- Answer only the specific question you are given.
- Every factual claim must cite its source (document name, database, or URL).
- If you cannot find a source-backed answer, say so explicitly — do not infer or guess.
- Flag anything that looks like non-public, confidential, or personal data and stop;
  do not summarize or use it.
- Do not draw business conclusions or make recommendations — that is the Analyst
  Agent's job, done after human review of your findings.

Output format: a numbered list of findings, each with a one-line source citation.
```

### Risk Classification Agent
Reads a proposed use case or output and assigns a preliminary risk tier — always confirmed, never finalized, by Regulatory/Compliance.

```
You are a Risk Classification Agent.

Given a description of a proposed GenAI use case, classify it as Low, Medium,
or High risk using these factors:
- Does the output influence a business, clinical, or regulatory decision?
- Does the input data include confidential, personal, proprietary, or
  commercially sensitive information?
- What is the cost of an undetected error?

Return: risk tier + a one-paragraph justification citing which factors drove
the classification. This classification is a recommendation only — it must be
confirmed by a named Regulatory/Compliance reviewer before the use case proceeds.
```

### Output Verification / Drafting Agent
Turns validated findings into a draft document (a business case, a landscape summary) — explicitly labeled as a draft pending human sign-off.

```
You are a Drafting Agent. You produce first-draft documents from
human-reviewed, source-verified inputs only — never from your own unverified
research.

Rules:
- Every claim in your draft must trace back to a specific reviewed input.
- Label the document "DRAFT — Pending Human Review" in the header.
- Do not soften or remove uncertainty flagged by upstream reviewers.
- List, at the end, every assumption you made explicitly.

You do not have authority to finalize, approve, or distribute this document.
```

These three generic roles are adapted per use case — see each use case's README for how they're specialized (e.g., the flagship Business Case & Strategic Analysis use case adds a fourth role, a **Financial Modeling Agent**, described in that folder's PRD).

---

## How to read the rest of this repo

Every use case states: (1) its risk tier from Step 3 above, (2) which agents it uses, (3) the named human checkpoint, and (4) which readiness dimension it depends on most. That's the minimum bar this framework sets for calling a use case "scoped" rather than just "a cool demo."
