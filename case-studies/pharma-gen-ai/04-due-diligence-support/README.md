# 04 — Due Diligence Support

**Risk Tier:** High — often touches counterparty-confidential data room material.

**Agents used:** Document Review Agent (specialized Research/Verification Agent, see [shared framework](../00-shared-framework/agentic-ai-framework.md)) — scoped to summarizing and flagging, never concluding.

**Human checkpoint:** Named diligence lead signs off on every flagged item before it's escalated or dismissed.

**Leans hardest on:** Data Governance Readiness — this is the use case in this repo where data classification and confidentiality controls are the whole ballgame, not a side concern.

## Scenario

During diligence on a potential licensing partner, Veridian Therapeutics (fictional) needs to triage a large data room — contracts, regulatory filings, IP documentation — faster than a fully manual first pass, while keeping legal privilege and confidentiality intact.

## What the AI does vs. what the human does

| Step | AI | Human |
|---|---|---|
| Summarize document contents and flag items matching a defined risk checklist (e.g. change-of-control clauses, IP encumbrances) | Document Review Agent | Diligence lead defines the checklist with Legal up front |
| Decide materiality of a flagged item | Agent flags, does not rank by materiality | Diligence lead and Legal judge materiality |
| Access to the data room itself | Runs only within an access-controlled environment matching existing data-room permissions — never a broader export | IT/Data Governance enforces access boundaries before any agent runs |

## Key design decision

The agent only ever *flags and summarizes* against a pre-agreed checklist — it never independently decides what's important. This is the one use case in the repo where I'd tell an interviewer I'd push back hardest on scope creep: the temptation to let the agent "just also" assess deal risk is exactly the kind of quiet mandate expansion that turns a document-triage tool into an unaccountable decision-maker.

## Guardrail

No document content or summary leaves the access-controlled environment it was reviewed in; the tool produces an internal flagged-items list, not an exportable report, until Legal has reviewed it.
