# PRD: Dark-Store Stockout Prevention Agent

## 1. Problem Statement

NovaMart Express operates dark stores carrying ~3,000 SKUs, promising 10–15 minute delivery. Customers who search for an item that shows "unavailable" typically switch to a competitor app within seconds — there is no browsing behavior to recover the sale, unlike a physical store or a next-day delivery model. Store ops teams currently rely on manual, twice-daily stock checks and reactive reordering, which means high-velocity SKUs (fast-moving snacks, dairy, beverages) stock out during peak windows before anyone notices.

## 2. Goal

Reduce stockout-driven lost sales on the top 20% of SKUs (by revenue) in a dark store, by giving store ops and category managers an earlier, more accurate signal of an impending stockout — with a human always in the loop for any action that commits money or shelf space.

## 3. Non-Goals

- This agent does not automatically place purchase orders without human approval.
- This agent does not manage overstock, markdowns, or cross-store allocation (see the shared governance doc for why those are scoped as separate agents).
- This is not a demand-forecasting model rebuild — it consumes forecast output as an input, it doesn't replace the forecasting team's model.

## 4. Target Users

- **Store Ops Lead** — acts on stockout alerts during a shift.
- **Category Manager** — sets thresholds and reviews weekly patterns.
- **Supply Chain Planner** — approves reorder trigger recommendations.

## 5. Success Metrics

- **Primary:** % reduction in stockout-hours on top-20% SKUs, measured store-by-store, month over month.
- **Secondary:** Lead time between "agent flags risk" and "human takes action" (target: under 30 minutes during peak hours).
- **Guardrail metric:** False-positive alert rate must stay under an agreed threshold, or store ops will start ignoring alerts entirely (alert fatigue is the primary failure mode of this product).

## 6. Scope (V1)

- In scope: single dark store, top-20% SKUs by revenue, alert + recommended-reorder-quantity output.
- Out of scope for V1: multi-store network view, auto-triggering purchase orders, new-SKU cold-start handling (SKUs with under 30 days of sales history are explicitly excluded from V1 and flagged as a known limitation).

## 7. Human-in-the-Loop Design

- The agent's output is always a **recommendation with a confidence score**, never a committed action, in V1.
- Store Ops Lead receives the alert and can accept, adjust quantity, or dismiss with a reason code.
- Dismissal reason codes feed back into a weekly review with the Category Manager (see shared RACI) to catch systematic false positives.
- A SKU only becomes eligible for a lighter-touch "auto-trigger with notify" mode after 8 consecutive weeks of >90% recommendation-acceptance rate — this graduation path is itself reviewed and signed off by the AI Governance Owner, not automatic.

## 8. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Alert fatigue from false positives | Confidence threshold tuned conservatively in V1; dismissal reasons tracked and reviewed weekly |
| Agent recommends unrealistic reorder quantities | Output is bounded by a simple rule (reorder qty within a defined multiple of trailing 4-week average) before being surfaced |
| Data lag (stock counts not real-time) | Store ops sees a "data freshness" timestamp on every alert; alerts older than a defined threshold are auto-suppressed rather than shown stale |

See [`agent-framework.md`](agent-framework.md) for how the agent itself is structured, and the shared [governance doc](../../docs/governance-and-raci.md) for oversight and audit design.
