# 02 — Market & Competitor Intelligence

**Risk Tier:** Medium — informs strategic awareness, not a standalone decision.
**Agents used:** Research Agent (see [shared framework](../00-shared-framework/agentic-ai-framework.md)), specialized for continuous competitor monitoring rather than one-off queries.
**Human checkpoint:** Commercial Strategy analyst reviews and annotates the weekly digest before it's distributed beyond the immediate team.
**Leans hardest on:** Process Readiness (this is a recurring, not one-off, output — without a review cadence it silently degrades into "trusted without checking").

## Scenario

Veridian Therapeutics (fictional) wants a standing view of competitor pipeline movement, pricing signals, and market entrants in its core therapeutic areas — refreshed weekly rather than researched from scratch each time a question comes up.

## What the AI does vs. what the human does

| Step | AI | Human |
|---|---|---|
| Scan approved sources (public filings, clinical trial registries, press releases) for material changes | Research Agent, run on a schedule | — |
| Distinguish "material" from "noise" | Agent proposes, flags confidence level | Analyst confirms before the digest goes out |
| Interpret competitive implications | — | Analyst and Commercial Strategy own this entirely |

## Key design decision

The agent is explicitly told to report only *changes since last run*, with a source and a confidence flag — not to re-synthesize the whole competitive landscape every week. That keeps the human review burden proportional to what's actually new, which is what makes a recurring use case sustainable rather than something people stop reading after week three.

## Guardrail

Any finding the agent can't confidently source gets held out of the digest and flagged for manual follow-up rather than included with a hedge — a wrong "maybe" in a competitive intelligence digest is worse than a gap.
