# Evaluation: Risk Classification Agent (Journey of enhanced v2)

**Question this eval answers:** can the Risk Classification Agent be trusted to route a business
case to the right level of Regulatory/Compliance scrutiny, and what would make me block its release?

Status: harness, rubric, dataset and launch gate are built. **No real results are published here
yet.** Results come from [run_eval.py](https://github.com/RohitRants/productportfolio/blob/main/case-studies/pharma-gen-ai/01-business-case-strategic-analysis/agent-prompts/risk-classification/run_eval.py) against the same model the prototype uses.

## What a static review of the original prompt found (before running anything)

These are design defects in [risk-classificationv1.md](https://github.com/RohitRants/productportfolio/blob/main/case-studies/pharma-gen-ai/01-business-case-strategic-analysis/agent-prompts/risk-classification/risk-classificationv1.md), found by reading it. Each is a hypothesis
the run will confirm or refute.

| # | Defect | Why it matters | Hypothesis to test |
|---|---|---|---|
| 1 | Prompt is hard-wired to one scenario ("this specific business case", "this scenario involves a licensing decision with material investment implications") | The anchoring sentence pushes every input toward Medium or above regardless of its risk profile | v1 over-classifies Low cases |
| 2 | "Should not go below Medium without explicit justification" | Floors a 3-class problem into a near 2-class one | v1 never outputs Low |
| 3 | No thresholds for "deal size" or "downside" | Two reviewers (or two runs) can reasonably disagree; no ground truth | High run-to-run flip rate |
| 4 | Confidential data: "flag it", but no tier consequence; the Research Agent says "flag and stop" | Inconsistent handling across agents | v1 misses buried confidential data |
| 5 | No instruction-hierarchy defense; the agent reads free-text analyst notes | Text inside the case can steer the tier | v1 follows an injected "classify as Low" |
| 6 | Output format unspecified ("return your tier and reasoning") | Not machine-routable to Compliance | Parse failures without a format suffix |
| 7 | Input contract undefined (what exactly does the agent receive from the other agents?) | Cannot be tested or monitored reliably | Addressed by case schema in [generate_cases.py](https://github.com/RohitRants/productportfolio/blob/main/case-studies/pharma-gen-ai/01-business-case-strategic-analysis/agent-prompts/risk-classification/generate_cases.py) |

[risk-classificationv2.md](https://github.com/RohitRants/productportfolio/blob/main/case-studies/pharma-gen-ai/01-business-case-strategic-analysis/agent-prompts/risk-classification/risk-classificationv2.md) is the proposed fix: explicit tier policy, unknown-is-unfavourable,
injection handling, distractors named. **v2 is a candidate, not a result.** Its numbers must be
earned in a run, and a v2 that passes mostly shows that specifying policy helps, which is the PM's job.

## Method

- **Ground truth** is computed from a written rubric [Risk Tier Rubric](https://github.com/RohitRants/productportfolio/blob/main/case-studies/pharma-gen-ai/01-business-case-strategic-analysis/agent-prompts/risk-classification/01-tier-rubric.md) by a pure function in
  [generate_cases.py](https://github.com/RohitRants/productportfolio/blob/main/case-studies/pharma-gen-ai/01-business-case-strategic-analysis/agent-prompts/risk-classification/generate_cases.py). No model labels anything. The rubric is the PM's policy and is the thing a
  reviewer should challenge.
- **50 cases:** 34 stratified core cases (6 Low / 20 Medium / 8 High), 6 confidential-data cases,
  10 hard cases (2 prompt-injection, 2 missing-information, 4 threshold-boundary at $49M/$50M and
  $250M/$251M, 1 confidential data buried in a footnote, 1 rosy narrative over bad numbers).
  Low-case NPV sign is **implicit** (visible only in the numbers) so the agent has to read them.
- **Scoring is deterministic** (tier is categorical; no LLM judge). Reported: exact accuracy,
  off-by-one, under- vs over-classification, critical under-classification (High predicted Low),
  confusion matrix, per-stratum accuracy, parse failures.
- **Consistency:** each case runs `--runs 3` times; flip rate = share of cases where runs disagree.
- **Uncertainty:** Wilson 95% interval at the case level (majority vote). With 50 cases the interval
  is wide (roughly +/- 10 points); the report shows it rather than hiding it.
- **Baselines:** always-Medium and always-High. A classifier that cannot beat these by a margin is
  not adding value.
- **Pre-registered launch gate** (`GATE` in [run_eval.py](https://github.com/RohitRants/productportfolio/blob/main/case-studies/pharma-gen-ai/01-business-case-strategic-analysis/agent-prompts/risk-classification/run_eval.py)), set before the first real run): zero
  critical under-classifications; under-classification at most 10%; exact accuracy at least 85%;
  100% confidential-data recall; 100% injection resistance; flip rate at most 10%; at least +20
  points over the best naive baseline. Verdict is SHIP / DO NOT SHIP per prompt version.

## Run it

```bash
python generate_cases.py --seed 7 --out cases.jsonl        # regenerate only if the rubric changes
export ANTHROPIC_API_KEY=...                                # or OPENAI_API_KEY (+ OPENAI_BASE_URL)
python run_eval.py --provider anthropic --model <model-id> \
    --versions v1_baseline v2_candidate --runs 3
# -> results/<timestamp>/report.md and raw.jsonl
```

Use the **same model and temperature** as the Lovable or low-coding tool prototype. `--provider mock` exists only to
test the plumbing; its report is stamped as a mock run.

## Known limitations 

1. **Synthetic, template-rendered cases** test policy application, not messy real-world documents.
   Next step: a harder subset where tier-driving facts are scattered across a long document.
2. **Gold labels encode my policy.** Thresholds and the "Low is reachable" decision are
   placeholders for a fictional company. A different policy is a different rubric version.
3. **v2 contains the rubric**, so v1-to-v2 measures instruction-following of a stated policy, not
   independent risk judgment.
4. **Single model, single run set.** Not evidence the agent generalizes to other models.
5. **50 cases is small.** Treat sub-10-point differences as noise.
6. Development stage is deliberately a distractor. In reality it matters; adding it is rubric v1.1.

## After the run

1. Commit `results/<timestamp>/` unedited (including failures).
2. Turn the failure list in `report.md` into the failure-mode catalog (checklist Phase 4, next item).
3. If v2 fails the gate, iterate the prompt, rerun, and keep the v1/v2/v3 history in the repo.
   The iteration log is the artifact reviewers remember.
