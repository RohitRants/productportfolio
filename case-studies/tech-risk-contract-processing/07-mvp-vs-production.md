# 07. MVP vs. Production

This is the section I want reviewers to read closely: I know this is a no-code MVP, not a production system. Here's exactly what separates the two — which is what I'd actually be accountable for as the PM shepherding this toward launch.

| Dimension | MVP (this repo) | Production |
|---|---|---|
| Data handling | Demo/synthetic contract data | Real contracts — requires encryption at rest/in transit, data residency controls, access logging |
| AI infrastructure | Lovable's built-in AI Gateway | Vetted enterprise LLM contract (data processing agreement, no training on bank data), likely private/VPC deployment |
| Regulatory scope | US only (OCC, FFIEC, NYDFS) | Multi-jurisdiction, versioned as regulations change |
| Human-in-the-loop | Manual review of flags | Formal sign-off workflow integrated with existing GRC/case-management systems |
| Auditability | Basic decision log | Full audit trail meeting regulatory examination standards |
| Integration | Standalone app | Integrated with contract lifecycle management (CLM) and vendor risk systems |
| Model governance | None (MVP) | Model risk management review (SR 11-7 equivalent), periodic bias/drift testing |
| Scale | Single contract at a time | Batch processing, SLA-backed throughput |

## Why I scoped it this way
*(One paragraph: the MVP proves the product concept and UX cheaply; production readiness is a distinct, resourced phase — and I know the difference.)*
