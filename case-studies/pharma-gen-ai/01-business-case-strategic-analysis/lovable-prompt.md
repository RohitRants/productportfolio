# Lovable AI Build Prompt — Business Case & Strategic Analysis MVP

Below prompt has been used in Lovable AI to generate the clickable prototype. the clickable prototype can be accessed from here [README.md](./README.md).

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

Through this prompt an end-to-end. Veridian Strategic Analysis Assistant is built — a six-stage wizard with a locked left-side stepper, verified in a real browser run with live AI Gateway calls:

**1. New Analysis** — target company (fictional OK), therapeutic area dropdown, Licensing/Acquisition/Partnership selector.

**2. Research Findings** — AI-generated table (Category | Finding | Source | Confidence) under an "AI-generated — review before proceeding" banner; each row needs a Reviewed check or explicit Dismiss before continuing (dismissed rows are excluded downstream).

**3. Financial Inputs** — five analyst-entered fields (peak sales, PTRS, discount rate, deal cost, timeline) with validation; deliberately never pre-filled from AI output.

**4. Financial Model** — rNPV computed deterministically so the displayed formula (rNPV = Σt [PeakSales(t) × Margin × PTRS ÷ (1+r)^t] − DealCost), input table, low/base/high range, and year-by-year cash-flow table always agree; Lovable AI writes the narrative, sensitivity commentary, and deal economics.

**5. Risk Classification** — AI Low/Medium/High verdict with written justification and key drivers, locked behind a "Confirmed by Compliance" checkbox (re-running classification resets the sign-off).

**6. Draft Business Case** — AI assembles all seven sections from only the reviewed findings and prior outputs, under a persistent **DRAFT — Pending Human Review** banner and striped watermark; "Mark as Final" stays disabled until a reviewer name is entered, then flips to a green FINAL banner.

**Tip for the interview:** be ready to explain, out loud, why the stepper locks each stage behind a human-review action — that's the one design decision in this prototype that most directly demonstrates the "human oversight" requirement from the [governance framework](../00-shared-framework/agentic-ai-framework.md), not just a generic AI SaaS wizard.

