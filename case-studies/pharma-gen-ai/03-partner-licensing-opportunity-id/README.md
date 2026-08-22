# 03 — Partner & Licensing Opportunity Identification

**Risk Tier:** Medium-High — surfaces candidates for real relationships and deal conversations.
**Agents used:** Research Agent, plus a scoring/ranking step (rules-based, not a black-box AI score — see below).
**Human checkpoint:** Business Development Director reviews the shortlist before any outreach is considered.
**Leans hardest on:** Human & Organizational Readiness — this use case fails if BD teams treat the shortlist as a to-do list rather than a starting point for their own judgment.

## Scenario

Licensing wants a standing shortlist of external assets or technologies that might fit Veridian Therapeutics' (fictional) strategic priorities, instead of relying on individual BD managers' personal networks and ad hoc searches.

## What the AI does vs. what the human does

| Step | AI | Human |
|---|---|---|
| Scan public sources for assets/companies matching defined strategic criteria | Research Agent | Licensing defines the criteria up front |
| Score fit against those criteria | Transparent, rules-based scoring (criteria weights are visible, not learned) | BD Director can override any score with a stated reason |
| Decide who to actually approach | — | Entirely a human relationship/timing/political judgment call, never delegated to AI |

## Key design decision

The "scoring" step is deliberately **not** a machine-learning ranking model — it's a transparent weighted checklist against criteria Licensing defines and can see. In a relationship-driven function like BD, an opaque score that BD can't interrogate erodes trust in the tool fast; a visible, editable rubric doesn't.

## Guardrail

The shortlist explicitly excludes any recommendation on deal terms, valuation, or approach strategy — those stay 100% human, every time, because they depend on relationship context no research agent has access to.
