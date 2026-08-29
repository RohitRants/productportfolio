# Retail AI Agent Portfolio — Rohit Kumar

## About Me

My strength is translating a fuzzy business problem into a scoped, governed, buildable AI product: defining the use case, mapping the data and stakeholders, designing the human-in-the-loop guardrails, and specifying what "good" looks like for both the business and the engineering team that has to build it.

**Why AI PM, and why retail:** Retail inventory is one of the clearest places where agentic AI creates measurable value *and* carries real operational risk if it's under-governed — a wrong reorder call empties a warehouse's working capital, a wrong stockout call loses a sale in the ten minutes a quick-commerce customer is willing to wait. That tension between velocity and control is exactly the kind of problem AI product management exists to solve.

**What this repo is:** A portfolio of AI-agent product specs for retail inventory management, built to interview-round depth rather than production-grade completeness. One use case (dark-store stockout prevention) is developed all the way to PRD + agent design + data model + a clickable prototype. The other two are one-pagers, showing breadth of thinking without diluting depth on the flagship.

**What this repo is not:** A working production system. No use case here claims enterprise-scale engineering; the code/prototype exists to demonstrate product thinking, not to be deployed.

---

## Project Index

| # | Use Case | Type | Depth |
|---|----------|------|-------|
| 1 | [Dark-Store Stockout Prevention Agent](use-cases/01-dark-store-stockout-agent/) | B2C — quick-commerce | **Flagship** — full PRD, agent framework, data model, mockups, live prototype |
| 2 | [Physical-Store Pincode-Level Assortment Agent](use-cases/02-physical-store-assortment/) | B2C — traditional retail | One-pager | 
| 3 | [B2B FMCG-to-Retailer Delivery Agent](use-cases/03-b2b-fmcg-delivery/) | B2B | One-pager | 

## Cross-Cutting Documents

- [Governance, Human Oversight & RACI](docs/governance-and-raci.md) — the shared AI Agent Readiness Framework, oversight controls, and stakeholder RACI applied across all three use cases above. Read this once; every use case references it rather than repeating it.

## How to Read This Repo

1. Start with the [flagship use case](use-cases/01-dark-store-stockout-agent/) — it's the deepest evidence of product thinking.
2. Read the [governance doc](docs/governance-and-raci.md) to see how oversight is designed once and reused, not bolted on per use case.
3. Skim the two one-pagers for breadth.

## Fictional Company Note

All case studies are written against **NovaMart Express**, a fictional composite quick-commerce/retail chain, rather than any real company. The problems, data patterns, and constraints are drawn from how quick-commerce and retail chains genuinely operate, but no proprietary or real company data is used or implied anywhere in this repo.
