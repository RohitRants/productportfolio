# RACI Matrix — GenAI Use Cases in Pharma Business Development

This RACI is shared across all six use cases in this repo. It maps the [9-step readiness process](./agentic-ai-framework.md) against the stakeholder roles who need to stay in the loop for any GenAI-supported BD activity.

**R** = Responsible (does the work) · **A** = Accountable (signs off, one owner only) · **C** = Consulted (input sought before decision) · **I** = Informed (told after decision)

| Step | BD Managers | BD Directors | Alliance Mgmt | Licensing | Commercial Strategy | Corporate Strategy | Digital/AI Transformation | Regulatory & Compliance (BD) |
|---|---|---|---|---|---|---|---|---|
| 1. Identify the Use Case | R | A | C | C | C | C | R | C |
| 2. Define Context of Use | R | A | C | C | C | I | C | C |
| 3. Classify the Risk | I | C | I | I | I | I | R | A |
| 4. Assess Data Adoption | I | I | C | C | I | I | R | A |
| 5. Establish Human Oversight | A | A | C | C | C | I | C | C |
| 6. Validate Outputs | R | A | R | R | C | I | C | C |
| 7. Document AI Use | R | I | I | I | I | I | A | C |
| 8. Monitor Performance | I | I | I | I | I | I | A | C |
| 9. Review and Update | C | C | C | C | C | C | A | R |

### How to read this in an interview

- **Only one "A" per row** — that's deliberate. If two roles are both marked Accountable for the same step, the RACI is broken; that's a common failure mode I'm explicitly designing against.
- Digital/AI Transformation owns the technical spine (risk classification tooling, documentation infrastructure, monitoring) but is never solely accountable for whether the *business* uses the output responsibly — that stays with BD Directors and Regulatory/Compliance.
- Regulatory & Compliance is Accountable for risk classification and data adoption assessment specifically because those are the two steps where getting it wrong has the highest downside — not because they own the whole process end to end.
