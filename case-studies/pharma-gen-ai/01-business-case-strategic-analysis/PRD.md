# PRD — AI-Assisted Business Case & Strategic Analysis

**Product:** GenAI-assisted business case builder for BD/Corporate Strategy
**Company:** Veridian Therapeutics (fictional/composite)
**Status:** MVP / proof-of-work — not production-ready
**Owner:** [Your name], AI Product Manager (candidate portfolio project)

---

## Part A — Business Case (for BD, Corporate Strategy, and Commercial stakeholders)

### 1. Problem

When Corporate Strategy evaluates a licensing or acquisition opportunity, the first-draft business case (market sizing, competitive landscape, deal economics, risk factors) takes 4–6 weeks of analyst time before it reaches the investment committee for a preliminary read. Two things are true at once: leadership wants a faster first look, and nobody wants a faster *wrong* first look — a business case that skips verification just moves the risk downstream to the investment committee meeting itself.

### 2. Goal

Cut the time-to-first-draft from weeks to days by having GenAI agents assemble a structured, source-cited first draft — while keeping every judgment call (market assumptions, competitive read, go/no-go framing) explicitly owned by a named human reviewer, not the model.

### 3. Non-goals

- This does not automate the investment decision.
- This does not replace the analyst — it replaces the blank-page problem, not the analyst's judgment.
- This is not connected to real deal data, real financial systems, or any live vendor in this MVP.

### 4. Users

- **Primary:** Corporate Strategy analysts (build the draft), Corporate Strategy Director (reviews and signs off)
- **Consulted:** Commercial Strategy, Licensing, Regulatory & Compliance (BD)

### 5. What the AI does vs. what the human does

| Step | AI | Human |
|---|---|---|
| Gather market size, competitor, and deal-comp data | Research Agent finds and cites sources | Analyst spot-checks a sample of citations |
| Build a preliminary financial model (NPV, deal economics ranges) | Financial Modeling Agent runs the calculation on human-approved inputs | Analyst supplies/approves every assumption before the model runs |
| Classify risk tier of the analysis itself | Risk Classification Agent proposes a tier | Regulatory/Compliance confirms |
| Draft the narrative business case document | Drafting Agent assembles the draft from reviewed inputs only | Corporate Strategy Director approves before distribution |

### 6. Success criteria for the MVP demo

- A reviewer can trace every number in the draft back to a source or an explicitly-labeled assumption.
- The draft is clearly marked "DRAFT — Pending Human Review" until signed off.
- The risk classification step runs and is visible before the draft is generated, not as an afterthought.

### 7. Key risks and mitigations

| Risk | Mitigation |
|---|---|
| Model treats a strategic assumption as fact | Financial Modeling Agent only runs on assumptions explicitly entered by a human — it never invents them |
| Draft "feels" final and skips scrutiny | Hard-coded "DRAFT — Pending Human Review" watermark until sign-off step is completed |
| Confidential deal terms entered into a general-purpose model | MVP uses only fictional/synthetic data; production version would require a data-handling review before any real deal data is entered (see Technical section) |

---

## Part B — Technical / Engineering Reviewer Section

### 8. Data flow

```
[Analyst inputs: deal parameters, target company, assumptions]
        │
        ▼
[Research Agent] ── queries approved sources (market databases, public filings) ──► [Cited findings]
        │
        ▼
[Human review: analyst confirms/edits findings + assumptions]
        │
        ▼
[Financial Modeling Agent] ── runs deterministic calculations on approved inputs only ──► [Model outputs: NPV range, deal economics]
        │
        ▼
[Risk Classification Agent] ── proposes risk tier ──► [Regulatory/Compliance confirms]
        │
        ▼
[Drafting Agent] ── assembles narrative from everything above, nothing else ──► [DRAFT document]
        │
        ▼
[Corporate Strategy Director sign-off] ──► [Finalized business case]
```

Every arrow after "Human review" only carries data that a human has already touched — the pipeline is designed so that no AI-generated number reaches the draft without a human checkpoint upstream of it.

### 9. Model choice (MVP)

- **Research and Drafting Agents:** general-purpose LLM (this MVP uses Lovable AI's built-in AI Gateway) — chosen for the MVP because the task is synthesis and drafting, not calculation, and speed-to-prototype mattered more than model selection at this stage.
- **Financial Modeling Agent:** deterministic calculation logic (not an LLM) — an NPV/deal-economics calculation should not be probabilistic. The "agent" framing here is about *when* it runs and *what inputs* it's allowed to touch, not about using a language model to do arithmetic.
- In a production build, the Research Agent would sit behind retrieval-augmented generation (RAG) against licensed market-intelligence databases rather than open web search, both for accuracy and for licensing compliance.

### 10. Guardrails implemented in the MVP

- Every Research Agent output requires an inline citation field; outputs without one are flagged, not silently accepted.
- The Financial Modeling Agent's inputs are locked to a human-editable form — the agent cannot pull its own assumptions from the Research Agent's output directly.
- The draft document cannot be exported/shared from the prototype until a "Reviewed by" field is completed.

### 11. What would need to change for production

- Real data-room and deal-data handling would require encryption-at-rest, access logging, and a data classification review (see [Data Governance Readiness](../00-shared-framework/agentic-ai-framework.md)) before any non-synthetic data touches the system.
- Model choice for the Research Agent would move to a governed, approved-vendor model per [AI Governance Readiness](../00-shared-framework/agentic-ai-framework.md) — not an open consumer-facing tool.
- Full audit logging (Step 7 of the framework) would need to be a system-of-record integration, not a manual note.

### 12. Out of scope for this MVP

Authentication/SSO, real financial data integration, multi-user concurrent editing, version history, and integration with an actual document management system.
