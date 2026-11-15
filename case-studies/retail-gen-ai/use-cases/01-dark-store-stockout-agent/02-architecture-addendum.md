# Addendum for retail `04-ai-architecture-guardrails.md`: what is AI and what is not

## The design decision

The original build prompt had the agent produce "a confidence score and a recommended reorder
quantity", with every number as hardcoded mock text, so no model was ever called. The first
fix I proposed asked the AI Gateway to generate the confidence score. That was wrong, and I
replaced it. A language model's stated confidence is not calibrated against outcomes, so showing it
as a measured score would be decoration. This portfolio already reasons the other way elsewhere (the
pharma Financial Modeling Agent is deterministic and may not guess), and retail now follows the rule.

| Element | Produced by | Why |
|---|---|---|
| Risk level, hours to stockout, sort order | Deterministic code | Auditable, repeatable, testable against a reference |
| Recommended reorder quantity | Deterministic code | Same |
| Confidence % | Deterministic data-reliability heuristic | Measurable inputs: sales volatility, promotion, data freshness, history length |
| Escalation to Supply Chain Planner (below 60%) | Deterministic rule on that score | Unchanged from the original design |
| Rationale sentence | LLM via AI Gateway, constrained | Language is what a model is good at |
| Accept / Adjust / Dismiss | Human | Unchanged. Nothing runs on load or on a timer |

## Guardrails on the AI step

1. **The model cannot change the decision.** It receives computed values and writes one or two sentences.
2. **Grounding check.** Every number in the rationale must match a computed value; otherwise the
   rationale is rejected and a labelled template is shown instead.
3. **No fake AI.** Timeout, invalid JSON, or rejection each show a template labelled as such. Only a
   rationale that passed the check carries the "AI-generated" badge.
4. **Withheld quantity stays withheld.** When escalated, the quantity is not passed to the model.
5. **Untrusted text.** Item names are data; instructions inside them are ignored.
6. **Triggered by a human click only,** and cached per SKU for the session.
7. **Auditable.** The audit trail shows inputs, computed outputs, model input and output, grounding
   result and latency for every recommendation.

## What is real and what is mock

| Part | Status |
|---|---|
| SKU sales, stock, lead times, promo flags | Synthetic mock data (10 SKUs) |
| Scoring logic | Real code, verified equal across a Python reference and the TypeScript module on all fields |
| Rationale | Real AI Gateway call with grounding check |
| Policy values (16 operating hours, 1 review day, 1 safety day, 60% escalation, volatility threshold 0.35, penalties) | Placeholder assumptions for a fictional store |

## Known limits (state these before a reviewer does)

- **The confidence % is not a probability.** It is a data-reliability heuristic, labelled as such in
  the tooltip. Calibrating it would need outcomes: whether alerts led to real stockouts, and
  Screen 3's dismissal rates are the natural data source. That is the production path.
- **Seven-day velocity** ignores promotions beyond a crude "use the higher 3-day rate" rule and
  captures weekly seasonality only through the volatility score.
- **Hours to stockout** assumes demand spread evenly across 16 operating hours.
- **Grounding checks numbers only**, not tone or usefulness. A real evaluation would extend the
  pharma eval pattern (rubric, gold labels, launch gate) to rationale quality.
- **Single model, ten SKUs.** This proves the architecture, not performance at scale.
