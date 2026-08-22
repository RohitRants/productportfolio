# 01 — Business Case & Strategic Analysis (Flagship)

**Risk Tier:** High — output directly informs go/no-go investment decisions.
**Agents used:** Research Agent, Financial Modeling Agent, Risk Classification Agent, Drafting Agent (all defined in [the shared framework](../00-shared-framework/agentic-ai-framework.md); Financial Modeling Agent is specific to this use case, defined below).
**Human checkpoint:** Corporate Strategy Director signs off before any business case leaves draft status.
**Leans hardest on:** Process Readiness — the deliverable is a recommendation, not a fact, so the audit trail of how it was reached matters as much as the recommendation itself.

## Why this is the flagship

Of the six use cases in this repo, this is the one where "the AI is right" is never the whole story — a business case can be internally consistent, well-sourced, and still wrong because of a strategic assumption a model has no way to evaluate. That gap between *what AI can validate* and *what only a human can judge* is exactly what an AI PM is hired to design around. The other five use cases in this repo are largely research/synthesis problems; this one forces explicit human judgment calls, which is why it gets the full treatment here.

## What's in this folder

- **[PRD.md](./PRD.md)** — the full product requirements doc, split into a business-facing section and a technical-reviewer section (data flow, model choice, guardrails).
- **[agent-prompts.md](./agent-prompts.md)** — the specific agent instructions used in this use case, extending the shared framework's generic roles.
- **[lovable-prompt.md](./lovable-prompt.md)** — the exact prompt used to build the working prototype in Lovable AI.
- **[mockups/](./mockups)** — screen-by-screen walkthrough of the prototype.

## Live prototype

🔗 *[Add your Lovable AI published app link here once built]*

## The scenario, in one paragraph

Veridian Therapeutics (fictional) is evaluating whether to license a Phase II oncology asset from a smaller biotech. Corporate Strategy needs a first-draft business case — market sizing, competitive positioning, deal economics, and risk factors — within days, not the usual six weeks, without skipping the verification steps that make a business case defensible in front of the investment committee.
