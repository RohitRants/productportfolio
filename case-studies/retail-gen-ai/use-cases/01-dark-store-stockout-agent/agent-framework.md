# Agent Framework: Dark-Store Stockout Prevention Agent

## Architecture Overview

A single-purpose agent, run on a schedule (every 30 minutes during store operating hours), with three logical steps: **Detect → Reason → Recommend**. It does not act autonomously in V1 (see PRD, Section 7).

```
[Inventory & POS data feed]
        ↓
[1. Detect] — flags SKUs approaching a stockout threshold
        ↓
[2. Reason] — checks against sales velocity, lead time, and known events (promotions, weather)
        ↓
[3. Recommend] — produces a reorder recommendation + confidence score + plain-language rationale
        ↓
[Store Ops Lead reviews in dashboard] → Accept / Adjust / Dismiss
```

## Agent Roles

| Step | Responsibility | Autonomy Level |
|---|---|---|
| Detect | Continuously monitor stock-vs-velocity ratio per SKU | Fully automated (read-only) |
| Reason | Contextualize the raw signal (is this a real risk or a data glitch/one-off spike) | Fully automated (read-only) |
| Recommend | Produce a human-readable recommendation with confidence score | Automated output, human-approved action |

## Sample Agent Prompt — Detect Step

```
You are a retail inventory monitoring agent for a quick-commerce dark store.

Given the following data for a single SKU:
- Current stock level
- Trailing 4-week daily sales velocity
- Supplier lead time (days)
- Time since last restock

Determine whether this SKU is at risk of stocking out before the next
scheduled restock window. Output only:
- risk_level: none | low | medium | high
- estimated_hours_to_stockout: <number>
- reason: <one sentence, plain language>

Do not recommend an order quantity at this step — that is a separate task.
```

## Sample Agent Prompt — Recommend Step

```
You are a retail replenishment recommendation agent.

You have been told this SKU is at "high" risk of stockout in
{estimated_hours_to_stockout} hours.

Given:
- Trailing 4-week average daily sales
- Current stock level
- Supplier minimum order quantity and lead time
- Any active promotion flags for this SKU this week

Recommend a reorder quantity and a confidence score (0-100).

Constraints:
- The recommended quantity must not exceed 3x the trailing 4-week
  average weekly sales, unless an active promotion flag is present.
- If confidence is below 60, output "escalate_to_human_review: true"
  instead of a specific quantity.
- Always include a one-sentence, plain-language rationale a
  non-technical store ops lead can act on without reading raw data.

Output format: JSON with fields
recommended_quantity, confidence_score, rationale, escalate_to_human_review
```

## Why Two Separate Prompts, Not One

Splitting "detect risk" from "recommend quantity" keeps each prompt auditable and testable independently — a governance reviewer can validate the risk-detection logic without also having to validate the quantity math, and either step can be swapped out (e.g., replacing the detection logic with a proper time-series model later) without touching the other.

## Escalation Path

Any output with `escalate_to_human_review: true`, or any SKU new enough to lack 30 days of sales history, routes directly to the Supply Chain Planner rather than showing a specific recommended quantity to Store Ops — this is the concrete implementation of the "Establish Human Oversight" step in the shared governance framework.
