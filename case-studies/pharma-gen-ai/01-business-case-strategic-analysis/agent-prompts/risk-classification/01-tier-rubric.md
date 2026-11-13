# Risk Tier Rubric v1.0 (the source of ground truth)

**Why this file exists.** The original Risk Classification Agent prompt named three criteria
(deal size, confidential data, downside if assumptions are wrong) but gave no thresholds, so
"correct" was undefined. Gold labels in this eval are **computed from this rubric, never from a
model's opinion**. The rubric is a PM policy decision, so it is versioned and defended here.

> Veridian Therapeutics is fictional. Thresholds below are **placeholder policy assumptions**,
> stated openly so a reviewer can challenge them. Changing a threshold means bumping the rubric
> version and regenerating `cases.jsonl`.

## Attributes (what a case varies on)

| Attribute | Values | Where it appears in the case text |
|---|---|---|
| Total committed deal value | $M number | Stated in deal terms, or "not yet determined" |
| Core therapeutic area | oncology, immunology = core (policy) | Stated in strategic-fit line |
| Real confidential data | yes / no | Data-provenance line (or buried in a footnote) |
| Low-case risk-adjusted NPV | negative / not negative | **Implicit**: only visible in the NPV numbers, never stated in words |
| Assumption support | validated / mixed / unsupported | Assumption-provenance line |

Distractors (deliberately **not** in the rubric; a correct agent ignores them): development
stage, counterparty name, geography, narrative tone of the analyst note.

## Decision table (first match wins)

1. **High** if ANY of:
   - real confidential/non-public counterparty data is or may be present
   - deal value > $250M AND (Low-case NPV negative OR assumptions unsupported)
   - Low-case NPV negative AND assumptions unsupported
2. **Low** only if ALL of:
   - deal value < $50M
   - therapeutic area not core
   - Low-case NPV not negative
   - assumptions validated
   - no confidential data
3. **Medium** otherwise.

**Unknown = unfavourable.** Missing deal value counts as > $250M; missing sensitivity range
counts as negative Low-case NPV; missing assumption provenance counts as unsupported; unclear
data provenance counts as possibly confidential.

## Severity ordering and error costs

Tiers are ordinal: Low < Medium < High. Errors are **asymmetric**:

- **Critical under-classification**: gold High, predicted Low. Unacceptable.
- **Under-classification**: predicted < gold. Compliance may never see a risky case.
- **Over-classification**: predicted > gold. Costs reviewer time only; tolerable in moderation.

## Decisions the PM must own before running (do not skip)

1. **Is Low reachable at all for a licensing decision?** The original prompt set a Medium floor.
   This rubric allows Low only under five simultaneous conditions. If you believe Low should be
   unreachable, delete rule 2 and make this a two-tier problem. Either is defensible, but you must
   state which and why.
2. **Thresholds ($50M / $250M).** Justify them (e.g., relative to a fictional R&D budget) in one sentence.
3. **Should development stage matter?** It is a distractor here. In reality, Phase 1 vs Phase 3
   changes technical risk. If you disagree with excluding it, add it as an attribute (rubric v1.1).
4. **Hand-review the labels.** Open `cases.jsonl`, read every case's gold tier, and overrule any
   you disagree with *by changing the rubric*, not by editing single labels.
