# Lovable AI Build Prompt — Dark Store Stockout Agent MVP

Below prompt has been used in Lovable AI to generate the clickable prototype. the clickable prototype can be accessed from here [README.md]

---

```
Build: NovaMart Express — Dark-Store Stockout Prevention Agent (Dashboard Prototype)
 
Context
 
Build a web app prototype for **NovaMart Express**, a fictional quick-commerce dark-store chain (10–15 minute delivery). The app is a **Store Ops dashboard** for an internal tool that flags SKUs at risk of stocking out and recommends reorder quantities — this is a decision-support tool for a human, not a fully autonomous system. No real customer-facing storefront is needed; this is an internal operations tool only.
 
Core Concept
 
A single-purpose AI agent monitors dark-store inventory and produces stockout-risk alerts with a confidence score and a recommended reorder quantity. A human (the Store Ops Lead) reviews each alert and can Accept, Adjust, or Dismiss it. Nothing is auto-executed — every action requires human approval in this version.
 
Users (design for these three, but only Screen 1 & 2 need full interactivity)
 
1. **Store Ops Lead** — works a live shift, needs to triage alerts fast.
2. **Category Manager** — reviews weekly patterns, sets thresholds.
3. **Supply Chain Planner** — receives escalations the agent isn't confident about.

Screens to Build
 
Screen 1 — Alert Feed (primary screen)
- A ranked list/table of at-risk SKUs, sorted by urgency (most urgent first).
- Each row: SKU name, product image placeholder, current stock level, risk badge (color-coded: green=none, yellow=low, orange=medium, red=high), estimated hours to stockout, and a "data freshness" timestamp (e.g., "Updated 12 min ago").
- Clicking/tapping a row expands to show the recommendation detail (Screen 2 content, inline or as a slide-over panel).
- Each expanded row has three buttons: **Accept**, **Adjust Quantity** (opens a small quantity input), **Dismiss** (requires selecting a reason from a dropdown: "False alarm", "Already reordered", "Discontinuing SKU", "Other").
- Include a summary strip at the top: total alerts today, accepted, dismissed, pending.
- Use a card-based or table layout — should feel scannable in under 10 seconds per item, like an operations tool, not a marketing dashboard.
Screen 2 — Recommendation Detail (can be a slide-over panel triggered from Screen 1, doesn't need to be a separate route)
- Shows: SKU name, a simple sparkline or bar chart of trailing 4-week daily sales velocity, current stock level, supplier lead time (days), active promotion flag (yes/no badge), recommended reorder quantity, and a confidence score shown as a percentage with a progress-bar style indicator.
- A plain-language rationale sentence, e.g., "Sales velocity has increased 40% this week; current stock will run out in approximately 6 hours at this rate."
- If confidence is below 60%, instead of a recommended quantity, show a banner: "Escalated to Supply Chain Planner — confidence too low for a direct recommendation," styled distinctly (e.g., amber banner) so it reads clearly as a different state, not a failure.
- A small "View audit trail" link/expandable section showing the raw inputs used (mock data is fine).
Screen 3 — Category Manager Weekly Review (separate route/tab)
- A simple summary view: total alerts this week, broken down by Accepted / Adjusted / Dismissed (a simple bar or donut chart is fine).
- A table of SKUs with high dismissal rates (the ones most likely to be false positives), each with a "View dismissal reasons" expandable list.
- A toggle switch per SKU labeled "Enable auto-trigger with notify," visually marked as requiring two sign-offs (show two checkboxes: "Category Manager approved" and "AI Governance Owner approved" — the toggle should only visually "activate" once both are checked). This is meant to visually communicate that autonomy upgrades require dual sign-off, not to be a real permission system.
Data / Mock Content
 
Populate all screens with realistic mock data for a dark store: SKU categories should be typical quick-commerce items (e.g., milk, bread, instant noodles, soft drinks, snacks, eggs). Include a mix of risk levels across the alert feed (don't make everything "high risk" — include several low/medium and a couple of "none" to show the tool isn't just an alarm generator). Include at least one SKU in the escalated/low-confidence state on Screen 2 so that state is visible without extra clicks.
 
Visual Tone
 
Clean, functional, operations-tool aesthetic — think a warehouse/logistics dashboard, not a consumer app. Use a restrained color palette where color is reserved for risk-level signaling (so the red/orange/yellow/green badges are meaningful, not decorative). Legible at a glance, since this is meant to be used quickly during a live shift.
 
Explicitly Do Not Build
 
- No real backend, no real inventory integration, no user authentication — mock/static data is fine throughout.
- No auto-execution of any action — every state change in the prototype should originate from a simulated human click, never happen automatically on load or on a timer.
- No customer-facing storefront or checkout flow — this is an internal ops tool only.

```
