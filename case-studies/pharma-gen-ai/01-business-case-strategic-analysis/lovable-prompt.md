# Lovable AI Build Prompt — Business Case & Strategic Analysis MVP

Paste the prompt below into Lovable AI to generate the clickable prototype. After it builds, publish it and paste the live link into this use case's [README.md](./README.md).

---

```
Build a web app called "Veridian Strategic Analysis Assistant" — an internal
tool for a pharmaceutical company's Corporate Strategy team to draft business
cases for licensing/acquisition opportunities, with AI assistance and explicit
human review checkpoints at every stage.

Screens needed:

1. New Analysis — a form to start a new business case: target company name
   (text, can be fictional), therapeutic area (dropdown), deal type
   (Licensing / Acquisition / Partnership).

2. Research Findings — call the AI Gateway to generate a structured findings
   table (Category | Finding | Source | Confidence) for market size,
   competitor landscape, and comparable deal terms, clearly labeled as
   "AI-generated — review before proceeding." Include a checkbox per row for
   the analyst to mark each finding as reviewed. Do not let the user proceed
   to the next screen until every row is checked or explicitly dismissed.

3. Financial Inputs — a form where the analyst manually enters: peak sales
   estimate, probability of technical/regulatory success (%), discount rate
   (%), estimated deal cost, timeline (years). Do not pre-fill these from the
   Research Findings screen — they must be entered by the user.

4. Financial Model Output — using the AI Gateway, calculate and display a
   risk-adjusted NPV, a low/base/high sensitivity range, and deal economics,
   showing the formula and inputs used alongside the result, not just the
   number.

5. Risk Classification — call the AI Gateway to classify this analysis as
   Low/Medium/High risk with a written justification, and require the user to
   select a "Confirmed by Compliance" checkbox before proceeding (this is a
   simulated human-in-the-loop step, no real integration needed).

6. Draft Business Case — call the AI Gateway to assemble a business case
   document (Executive Summary, Market Overview, Competitive Landscape, Deal
   Economics, Risk Factors, Recommendation Options, Assumptions Appendix)
   using only the reviewed findings and financial outputs from prior screens.
   Display a persistent "DRAFT — Pending Human Review" watermark/banner at
   the top of this screen. Include a "Reviewed by" name field and a "Mark as
   Final" button that is disabled until that field is filled in.

Design: clean, professional, muted color palette appropriate for an internal
enterprise tool (not consumer-app styling). Use a left-side stepper showing
all six stages so the user always knows where they are in the process and
that later stages are locked until earlier human-review steps are complete.

Use the built-in AI Gateway for all AI-generated content (Research Findings,
Financial Model Output narrative, Risk Classification, Draft Business Case).
Use fictional/placeholder data throughout — do not connect to any real
company data source.
```

---

**Tip for the interview:** be ready to explain, out loud, why the stepper locks each stage behind a human-review action — that's the one design decision in this prototype that most directly demonstrates the "human oversight" requirement from the [governance framework](../00-shared-framework/agentic-ai-framework.md), not just a generic AI SaaS wizard.

