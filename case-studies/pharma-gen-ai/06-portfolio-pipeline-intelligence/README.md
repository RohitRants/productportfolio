# 06 — Portfolio & Pipeline Intelligence

**Risk Tier:** Medium — internal-facing, but touches cross-functional data with varying sensitivity.

**Agents used:** Research/Aggregation Agent, scoped to internal-approved data sources only (no external web search for this use case).

**Human checkpoint:** Portfolio management lead confirms any cross-program comparison before it's shared outside the immediate portfolio team.

**Leans hardest on:** AI Governance Readiness — this is the use case most likely to quietly expand into "connect the agent to everything," which is exactly what the framework's use-case registration step (Step 1/7) exists to prevent.

## Scenario

Corporate Strategy wants a consolidated view of how Veridian Therapeutics' (fictional) internal pipeline programs compare on stage, projected timeline, and strategic priority — pulled from existing internal tracking systems rather than manually reassembled for each leadership review.

## What the AI does vs. what the human does

| Step | AI | Human |
|---|---|---|
| Aggregate and normalize data already entered into approved internal systems (no new data collection) | Aggregation Agent | Portfolio team maintains the source systems as the single source of truth |
| Surface patterns (e.g., timeline clustering, resource concentration) | Agent flags patterns with the underlying data shown alongside | Portfolio lead interprets whether a pattern is meaningful or coincidental |
| Recommend portfolio prioritization or reallocation | — | Always a leadership-level strategic call, never delegated to the agent |

## Key design decision

This agent is scoped to *read from* existing internal systems of record, not to become a new parallel source of truth. Every aggregated figure links back to its origin system rather than being restated as a new number — so if the underlying tracker changes, the intelligence view doesn't silently drift out of sync with reality.

## Guardrail

Access to program-level data is scoped per the same access permissions as the underlying source systems — the agent doesn't grant a viewer access to anything they couldn't already see directly, it only makes what they're already entitled to see easier to compare.

