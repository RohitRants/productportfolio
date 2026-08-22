# 05 — Scientific & Technology Landscape Analysis

**Risk Tier:** Medium — informs strategic direction, but sits closer to research synthesis than deal execution.

**Agents used:** Research Agent, specialized to weight peer-reviewed and regulatory sources over general web content.

**Human checkpoint:** A named scientific/medical reviewer (not just a BD analyst) validates any clinical or mechanistic claim before it's used externally.

**Leans hardest on:** Process Readiness for output verification — scientific claims carry a different credibility bar than market or competitive claims.

## Scenario

Corporate Strategy and R&D leadership want a synthesized view of an emerging modality or technology platform (e.g., a novel delivery mechanism) to inform whether it's worth active scouting — without commissioning a full external scientific review for every early-stage question.

## What the AI does vs. what the human does

| Step | AI | Human |
|---|---|---|
| Synthesize published literature, patent filings, and conference abstracts on a defined technology area | Research Agent | Scientific reviewer defines scope and key questions up front |
| Flag scientific claims and their evidentiary strength | Agent labels each claim's source type (peer-reviewed / preprint / conference abstract / company press release) | Scientific reviewer weighs evidentiary strength in the final read |
| Draw a conclusion about strategic relevance | — | Always a named scientific/medical + strategy joint call, never the agent alone |

## Key design decision

The agent is required to tag the *evidentiary tier* of every source (peer-reviewed vs. preprint vs. press release) rather than presenting all findings with equal confidence — because in a scientific context, treating a company press release and a peer-reviewed paper as equally credible is a specific, avoidable failure mode, not a generic "AI hallucination" concern.

## Guardrail

The agent is explicitly instructed not to draw mechanistic or efficacy conclusions itself — only to surface and label evidence. That interpretive step is reserved for a qualified scientific reviewer, every time.
