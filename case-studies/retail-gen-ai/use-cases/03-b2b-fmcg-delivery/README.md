# One-Pager: B2B FMCG-to-Small-Retailer Delivery Agent

**Company:** NovaMart Express Wholesale (fictional composite B2B arm)
**Problem type:** Allocation/forecasting — matching FMCG supply to small independent retailer demand across a distribution network.

## Problem

A B2B FMCG distributor serving small independent retailers (kirana-style stores) needs to forecast and allocate limited supply across many small accounts, each with irregular order patterns and inconsistent digital order history compared to a single large retailer.

## Proposed Agent

A demand-forecasting-and-allocation agent that recommends how much of a constrained SKU (e.g., during a supply shortage or high-demand period) should be allocated to each small retailer account, based on their historical order pattern and account tier — surfaced to a B2B Account Manager for approval before any allocation is committed.

## Key Difference from the Flagship

- **Data quality challenge:** Small retailer accounts often have thinner, noisier order history than a single dark store's POS data — the agent's confidence-scoring approach from the flagship becomes even more important here, since data sparsity is the norm rather than the exception.
- **Fairness/equity consideration:** Allocation decisions across many small accounts raise a fairness dimension the flagship doesn't have to deal with — the agent's recommendation logic needs an explicit, auditable rule for how ties or scarcity are resolved across accounts, not just an accuracy optimization.

## Governance

Assessed against the same shared [Governance, Human Oversight & RACI](../../docs/governance-and-raci.md) framework, with the B2B Account Manager as the accountable role for allocation sign-off.

## Status

Scoped at one-pager depth for this portfolio; not built out into a full PRD, agent framework, or prototype.
