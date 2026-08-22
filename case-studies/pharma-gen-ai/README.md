[README.md](https://github.com/user-attachments/files/31333267/README.md)
# GenAI in Pharma Business Development — An AI Product Manager Portfolio

## About me

*[Your name] — AI Product Manager | 5+ years in [your domain, e.g. enterprise SaaS / fintech / healthcare ops]*

I'm not from a pure engineering background, and this repo isn't trying to pretend otherwise. What I bring is product judgment: the ability to take an ambiguous, high-stakes business problem, decide what an AI system should and shouldn't be trusted to do, and design the guardrails, review points, and stakeholder workflow around it so the thing actually survives contact with Legal, Compliance, and Regulatory Affairs.

This repo is my answer to "show me you can do AI product management in a regulated industry" — specifically pharmaceutical business development, where the upside of GenAI (faster market scans, faster due diligence, faster business cases) is real, but so is the downside of an ungoverned model touching confidential deal data or making an unverified claim that ends up in a board deck.

**Why pharma BD:** it's a domain where product management is inseparable from risk management. Every use case below has to answer "who is accountable if this is wrong" before it answers "what does the UI look like."

## How this repo is organized

All six use cases below come from a single proposed framework: a risk-tiered, human-in-the-loop approach to introducing agentic AI into pharma BD workflows, without asking any one team to boil the ocean.

| # | Use Case | Depth | What it demonstrates |
|---|---|---|---|
| 01 | [Business Case & Strategic Analysis](./01-business-case-strategic-analysis) | **Flagship** — full PRD, agent prompts, clickable prototype | End-to-end product thinking: problem framing, AI/human division of labor, guardrails, and a working artifact |
| 02 | [Market & Competitor Intelligence](./02-market-competitor-intelligence) | One-pager | Scoping a research-agent use case with source-verification built in |
| 03 | [Partner & Licensing Opportunity Identification](./03-partner-licensing-opportunity-id) | One-pager | Matching AI output to a high-stakes, relationship-driven BD workflow |
| 04 | [Due Diligence Support](./04-due-diligence-support) | One-pager | Confidentiality and data-room sensitivity as first-order design constraints |
| 05 | [Scientific & Technology Landscape Analysis](./05-scientific-technology-landscape-analysis) | One-pager | Bridging scientific credibility with AI-generated synthesis |
| 06 | [Portfolio & Pipeline Intelligence](./06-portfolio-pipeline-intelligence) | One-pager | Internal-facing intelligence with cross-functional data sensitivity |

Cutting across all six:

- **[Agentic AI Governance Framework](./00-shared-framework/agentic-ai-framework.md)** — the 9-step Regulatory AI Agent Readiness process, the 6 readiness dimensions, and sample agent instructions, applied consistently across every use case.
- **[RACI Matrix](./00-shared-framework/RACI-matrix.md)** — how Business Development, Alliance Management, Licensing, Commercial/Corporate Strategy, Digital/AI Transformation, and Regulatory/Compliance stay in the loop at each stage.

## A note on realism

Every scenario, company name, and figure in this repo is fictional or composite (**"Veridian Therapeutics"**), built to be representative of pharma BD workflows without referencing or disclosing any real company's actual practices, data, or confidential information. Nothing here is production-ready — that's intentional; the point is to show product and governance thinking, not to ship code.

## Start here

If you only read one thing, read the [flagship PRD](./01-business-case-strategic-analysis/PRD.md) — then the [agentic framework](./00-shared-framework/agentic-ai-framework.md) it's built on.
