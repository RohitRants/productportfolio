# Rohit Kumar Portfolio

**Three case studies on shipping AI agents where a confident wrong answer is expensive: pharma business development, retail inventory, and bank technology risk.** Each has a PRD, an agent architecture with named guardrails, a clickable prototype, and an explicit account of what separates the demo from production. The pharma Risk Classification Agent also has a pre-registered evaluation with a ship / no-ship gate.

> **Scope** These are scoped MVP proofs of concept, not production systems. Every company, deal and dataset is fictional or built from public information, and nothing here uses employer data, systems or confidential material.

## Start here (2 minutes)

1. **Test of judgment:** [Evaluation of the Risk Classification Agent](https://github.com/RohitRants/productportfolio/tree/main/case-studies/pharma-gen-ai/01-business-case-strategic-analysis/agent-prompts/risk-classification). A written risk policy, 50 cases with rubric-derived labels, naive baselines, and a launch gate fixed before the run.
2. **Working prototype:** [Pharma business-case assistant](https://corp-strategy-aid.lovable.app/).
3. **How I frame a problem:** open any case study below and read `01-problem-framing.md` first.

## Resources

| # | Prompts | Use |  
|---|---|---|
| 1 | [Create Roadmaps, PRDs, Mockups](./resources/01-operational/) | System prompt for everyday product work |
| 2 | [Agent Evaluation Harness]() | Reusable pattern: policy rubric, computed gold labels, deterministic scoring, pre-registered launch gate |

## Case Studies

| # | Case Study | Domain |  
|---|---|---|
| 1 | [GenAI in Pharma Business Development](./case-studies/pharma-gen-ai) | Pharmaceutical Industry - Business Development |
| 2 | [Gen AI in Retail Inventory Management](./case-studies/retail-gen-ai) | Retail Industry - Inventory Management |
| 3 | [Tech Risk Contract Processing](./case-studies/tech-risk-contract-processing/) | Investment Banking - Technology Risk | 

## Why these 3 industries

I chose pharma business development, retail inventory and bank technology risk because they share one failure shape: decisions with real money or compliance consequences, inputs that are messy or confidential, and humans who must stay accountable. The same design pattern recurs in all three: narrow single-purpose agents, human-approved inputs, a named owner for every escalation, and a metric that can fail. That pattern, not the industry, is the transferable skill.

## Why this structure

Most AI PM case studies stop at "here's a cool demo." I wanted mine to also answer the questions a hiring panel actually probes for:

- **Why this problem, and why now** → Problem Framing
- **Who else needs to be in the room** → Stakeholders and RACI
- **What tradeoffs did you make, and why** → Product Decisions
- **How do you prevent this AI system from doing something dangerous or wrong** → AI Architecture and Guardrails
- **Can you actually direct a build, not just talk about one** → MVP Build Prompt + Mockups
- **Do you understand the gap between a demo and a real system** → MVP vs Production
- **How would you know if this succeeded** → Success Metrics and KPIs

## Roadmap (what I am building next, in order)

1. Failure-mode catalog built from the evaluation's actual failures
2. Cost and latency table for the agents' model choices
3. Teardown of a shipped AI product, with failure modes I found by probing it myself

## About me

I lead cross-functional delivery at Morgan Stanley, working with **25+** engineers and **4+** stakeholder groups on a bi-weekly release cadence. {{ONE_OUTCOME_WITH_BEFORE_AND_AFTER_NUMBER}}. 

**Why AI PM** This portfolio is me practicing that in public: scoped AI agents with named guardrails, human approval points, and evaluations that can fail. I am looking for AI Product Manager roles where shipping safely matters as much as shipping fast.

## Contact

*[Linkedin](https://www.linkedin.com/in/rohit--kumar/)*
