# One-Pager: Physical-Store Pincode-Level Assortment Agent

**Company:** NovaMart Express (fictional composite)
**Problem type:** Allocation — matching store-level assortment to hyperlocal (pincode-level) demand patterns in traditional physical stores.

## Problem

Unlike a dark store, a physical store carries tens of thousands of SKUs across a large footprint, and demand varies meaningfully by pincode-level demographics and local preferences. Static, chain-wide assortment planning under-serves local demand and ties up shelf space and working capital in SKUs that don't move in a given location.

## Proposed Agent

An assortment-recommendation agent that ingests store-level sales history and pincode demographic/demand signals, and recommends localized assortment adjustments (add/drop/resize SKU allocation) for a Category Manager to review on a monthly planning cadence — not a real-time agent like the flagship, since assortment changes operate on a slower cycle than stockout prevention.

## Key Difference from the Flagship

- **Cadence:** Monthly/quarterly planning decision, not a real-time alert — much lower time pressure, but higher financial stakes per decision (shelf space and inventory investment, not a single missed sale).
- **Human oversight:** Every recommendation requires Category Manager sign-off before any assortment change is executed — there is no "auto-trigger" graduation path for this use case, given the higher cost of a wrong call.

## Governance

Assessed against the same shared [Governance, Human Oversight & RACI](../../docs/governance-and-raci.md) framework as the flagship, with the Category Manager as the accountable role for assortment sign-off.

## Status

Scoped at one-pager depth for this portfolio; not built out into a full PRD, agent framework, or prototype.
