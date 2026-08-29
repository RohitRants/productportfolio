# Data Model: Dark-Store Stockout Prevention Agent

## Input Data Requirements

Per the shared input-data guidance: 12–18 months of clean sales history, at SKU × store × date granularity, focused on the top 20% of SKUs by revenue (the 80/20 rule — this subset typically drives the large majority of dark-store revenue and nearly all of the stockout-sensitive demand).

| Field | Description | Source System |
|---|---|---|
| `sku_id` | Unique product identifier | POS / catalog |
| `store_id` | Dark-store identifier | Store master data |
| `date` | Transaction date | POS |
| `units_sold` | Daily units sold | POS |
| `current_stock_level` | Real-time or near-real-time stock count | Inventory management system |
| `supplier_lead_time_days` | Days between order placement and delivery | Procurement/ERP |
| `supplier_min_order_qty` | Minimum order quantity per supplier contract | Procurement/ERP |
| `promotion_flag` | Whether the SKU is under an active promotion this week | Marketing/promo calendar |
| `last_restock_timestamp` | When the SKU was last replenished | Inventory management system |

## Why Top-20%-of-SKUs, Not All SKUs (V1)

- Concentrates the agent's value on the SKUs where a stockout is both most likely (highest velocity) and most costly (highest revenue contribution).
- Keeps the human review workload manageable for a Store Ops Lead handling a single shift — a full-catalog alert feed would itself cause the alert fatigue this product is trying to avoid.
- Long-tail SKUs (bottom 80%) are explicitly a "V2 candidate," not a current gap — noted as a known limitation in the PRD.

## Data Differences: Mid-Size/D2C vs. Large Omnichannel Retailer

This matters for how a candidate use case would need to be adapted if pitched at a different company:

- **Mid-size / D2C dark-store operator:** Often has less mature POS-to-inventory system integration; stock-level data may lag by hours rather than being near-real-time. The agent's "data freshness" check (see PRD risk table) becomes more important, not less.
- **Large omnichannel retailer (e.g., Walmart/Target scale):** Has vastly more historical data and typically real-time inventory feeds, but SKU count and store count are orders of magnitude larger — the top-20% cut is a much larger absolute number of SKUs, and cross-store/cross-format effects (a SKU stocking out in a dark store vs. its supercenter counterpart) become a real V2 consideration this V1 explicitly excludes.

## Data This Agent Does Not Use

To keep the governance story clean: no personal customer data, no loyalty/PII fields, and no payment data are used anywhere in this pipeline — inputs are entirely SKU-, store-, and supplier-level, which is why this use case is classified as commercially sensitive but not privacy-sensitive in the shared governance doc.
