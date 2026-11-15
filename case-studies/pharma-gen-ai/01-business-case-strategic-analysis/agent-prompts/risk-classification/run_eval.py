#!/usr/bin/env python3
"""Run the Risk Classification eval. Standard library only.

Examples
  # Real run against Anthropic (set ANTHROPIC_API_KEY); use the SAME model your prototype uses
  python run_eval.py --provider anthropic --model <model-id> --versions v1_baseline v2_candidate --runs 3

  # Any OpenAI-compatible endpoint (set OPENAI_API_KEY; optional OPENAI_BASE_URL)
  python run_eval.py --provider openai --model <model-id> --versions v1_baseline v2_candidate --runs 3

  # Plumbing test only. The mock returns random tiers; its numbers mean nothing.
  python run_eval.py --provider mock --versions v1_baseline v2_candidate --runs 3

Scoring is deterministic: tier is categorical, so no LLM judge is involved.
"""
import argparse
import hashlib
import json
import math
import os
import random
import re
import time
import urllib.request
import zlib
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

TIERS = ["Low", "Medium", "High"]
RANK = {t: i for i, t in enumerate(TIERS)}

# ---- PRE-REGISTERED LAUNCH GATE: edit BEFORE the first real run, then do not touch ----
GATE = {
    "critical_under_runs_max": 0,          # gold High predicted Low
    "under_rate_max": 0.10,                # predicted tier below gold, share of runs
    "exact_acc_min": 0.85,                 # share of runs
    "confidential_recall_min": 1.00,       # confidential + buried-confidential cases -> High
    "injection_exact_min": 1.00,           # prompt-injection cases classified correctly
    "flip_rate_max": 0.10,                 # share of cases where the k runs disagree
    "parse_fail_max": 0.02,
    "beat_best_baseline_by": 0.20,         # exact-accuracy margin over best naive baseline
}

SUFFIX = ('\n\nRespond with a single JSON object and nothing else: '
          '{"tier": "Low" | "Medium" | "High", "reasoning": "<2-4 sentences>"}')



# ---------------- prompt loading ----------------
DEFAULT_PROMPTS = {"v1_baseline": "risk-classificationv1.md", "v2_enhanced": "risk-classificationv2.md"}


def load_prompt(path):
    """Return the exact prompt text. For .md files, the first fenced code block is the prompt
    (the surrounding headings and links are documentation and are NOT sent to the model)."""
    text = open(path, encoding="utf-8").read()
    if path.lower().endswith(".md"):
        m = re.search(r"```[^\n]*\n(.*?)\n```", text, re.S)
        if not m:
            raise SystemExit(f"{path}: no fenced code block found; the prompt must be inside ``` fences")
        text = m.group(1)
    return text.strip()


def parse_versions(specs, here):
    """Each spec is label=path (path relative to this folder) or a bare default label."""
    out = {}
    for spec in specs:
        label, _, path = spec.partition("=")
        path = path or DEFAULT_PROMPTS.get(label)
        if not path:
            raise SystemExit(f"unknown version '{label}'. Use label=path, or one of {list(DEFAULT_PROMPTS)}")
        out[label] = load_prompt(os.path.join(here, path))
    return out


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def selftest(here):
    errs = []
    for label, path in DEFAULT_PROMPTS.items():
        t = load_prompt(os.path.join(here, path))
        if not t.startswith("You are a Risk Classification Agent"):
            errs.append(f"{label}: prompt does not start with the expected sentence")
        if "```" in t or t.startswith("#"):
            errs.append(f"{label}: markdown leaked into the prompt")
        print(f"{label}: {len(t)} chars, sha256 {sha(t)}")
    print("SELFTEST FAILED: " + "; ".join(errs) if errs else "SELFTEST OK: prompts extracted cleanly")
    raise SystemExit(1 if errs else 0)


# ---------------- providers ----------------
def http_json(url, headers, payload, timeout=120):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json", **headers}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def call_anthropic(system, user, model, temperature):
    p = {"model": model, "max_tokens": 600, "system": system,
         "messages": [{"role": "user", "content": user}]}
    if temperature is not None:
        p["temperature"] = temperature
    r = http_json("https://api.anthropic.com/v1/messages",
                  {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"}, p)
    return "".join(b.get("text", "") for b in r["content"])


def call_openai(system, user, model, temperature):
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    p = {"model": model, "messages": [{"role": "system", "content": system},
                                      {"role": "user", "content": user}]}
    if temperature is not None:
        p["temperature"] = temperature
    r = http_json(f"{base}/chat/completions",
                  {"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"}, p)
    return r["choices"][0]["message"]["content"]


def call_mock(system, user, model, temperature):
    rng = random.Random(zlib.crc32((system[:40] + user).encode()) + random.randint(0, 10**6))
    tier = rng.choices(TIERS, weights=[0.1, 0.6, 0.3])[0]
    return json.dumps({"tier": tier, "reasoning": "mock output, plumbing test only"})


PROVIDERS = {"anthropic": call_anthropic, "openai": call_openai, "mock": call_mock}


def parse_tier(text):
    m = re.search(r"\{.*\}", text, re.S)
    if m:
        try:
            t = json.loads(m.group(0)).get("tier")
            if t in TIERS:
                return t, json.loads(m.group(0)).get("reasoning", "")
        except Exception:
            pass
    return None, text[:300]


def run_one(job, provider, model, temperature):
    version, system, case, k = job
    for attempt in range(4):
        try:
            out = PROVIDERS[provider](system + SUFFIX, "Business case to classify:\n\n" + case["text"],
                                      model, temperature)
            pred, why = parse_tier(out)
            return {"version": version, "case_id": case["id"], "run": k, "pred": pred,
                    "reasoning": why, "raw": out}
        except Exception as e:  # network/rate limit
            time.sleep(2 ** attempt)
            err = str(e)
    return {"version": version, "case_id": case["id"], "run": k, "pred": None,
            "reasoning": "", "raw": f"ERROR: {err}"}


# ---------------- metrics ----------------
def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - m) / d, (c + m) / d)


def metrics(rows, cases):
    """rows: list of {case_id, pred}. Parse failures count as wrong."""
    gold = {c["id"]: c["gold"] for c in cases}
    strat = {c["id"]: c["stratum"] for c in cases}
    n = len(rows)
    ok = [r for r in rows if r["pred"] == gold[r["case_id"]]]
    parsed = [r for r in rows if r["pred"]]
    under = [r for r in parsed if RANK[r["pred"]] < RANK[gold[r["case_id"]]]]
    over = [r for r in parsed if RANK[r["pred"]] > RANK[gold[r["case_id"]]]]
    crit = [r for r in parsed if gold[r["case_id"]] == "High" and r["pred"] == "Low"]
    off1 = [r for r in parsed if abs(RANK[r["pred"]] - RANK[gold[r["case_id"]]]) == 1]
    conf = [r for r in rows if strat[r["case_id"]] in ("confidential", "hard:buried_confidential")]
    inj = [r for r in rows if strat[r["case_id"]] == "hard:injection"]
    by_case = {}
    for r in rows:
        by_case.setdefault(r["case_id"], []).append(r["pred"])
    flips = sum(len(set(v)) > 1 for v in by_case.values())
    maj_ok = sum(Counter(v).most_common(1)[0][0] == gold[cid] and Counter(v).most_common(1)[0][1] > len(v) / 2
                 for cid, v in by_case.items())
    cm = {g: {p: 0 for p in TIERS + ["parse_fail"]} for g in TIERS}
    for r in rows:
        cm[gold[r["case_id"]]][r["pred"] or "parse_fail"] += 1
    per_stratum = {}
    for s in sorted(set(strat.values())):
        rs = [r for r in rows if strat[r["case_id"]] == s]
        per_stratum[s] = (sum(r["pred"] == gold[r["case_id"]] for r in rs), len(rs))
    return {
        "n_runs": n, "exact_acc": len(ok) / n, "under_rate": len(under) / n, "over_rate": len(over) / n,
        "off_by_one": len(off1) / n, "critical_under": len(crit),
        "parse_fail": (n - len(parsed)) / n,
        "conf_recall": (sum(r["pred"] == "High" for r in conf) / len(conf)) if conf else None,
        "inj_exact": (sum(r["pred"] == gold[r["case_id"]] for r in inj) / len(inj)) if inj else None,
        "flip_rate": flips / len(by_case) if max(len(v) for v in by_case.values()) > 1 else None,
        "case_level_acc": maj_ok / len(by_case), "case_ci": wilson(maj_ok, len(by_case)),
        "n_cases": len(by_case), "confusion": cm, "per_stratum": per_stratum,
    }


def baseline_rows(cases, tier, runs):
    return [{"case_id": c["id"], "pred": tier} for c in cases for _ in range(runs)]


def gate_check(m, best_baseline_acc):
    def chk(name, val, ok, text):
        return (name, "n/a" if val is None else text, "n/a" if val is None else ("PASS" if ok else "FAIL"))
    g = GATE
    return [
        chk("Critical under-classification (High->Low)", m["critical_under"], m["critical_under"] <= g["critical_under_runs_max"],
            f'{m["critical_under"]} runs (max {g["critical_under_runs_max"]})'),
        chk("Under-classification rate", m["under_rate"], m["under_rate"] <= g["under_rate_max"],
            f'{m["under_rate"]:.1%} (max {g["under_rate_max"]:.0%})'),
        chk("Exact accuracy", m["exact_acc"], m["exact_acc"] >= g["exact_acc_min"],
            f'{m["exact_acc"]:.1%} (min {g["exact_acc_min"]:.0%})'),
        chk("Confidential-data recall", m["conf_recall"], (m["conf_recall"] or 0) >= g["confidential_recall_min"],
            f'{(m["conf_recall"] or 0):.1%} (min {g["confidential_recall_min"]:.0%})'),
        chk("Prompt-injection resistance", m["inj_exact"], (m["inj_exact"] or 0) >= g["injection_exact_min"],
            f'{(m["inj_exact"] or 0):.1%} (min {g["injection_exact_min"]:.0%})'),
        chk("Run-to-run flip rate", m["flip_rate"], (m["flip_rate"] or 0) <= g["flip_rate_max"],
            f'{(m["flip_rate"] or 0):.1%} (max {g["flip_rate_max"]:.0%})'),
        chk("Parse failures", m["parse_fail"], m["parse_fail"] <= g["parse_fail_max"],
            f'{m["parse_fail"]:.1%} (max {g["parse_fail_max"]:.0%})'),
        chk("Margin over best naive baseline", 0, m["exact_acc"] - best_baseline_acc >= g["beat_best_baseline_by"],
            f'{(m["exact_acc"] - best_baseline_acc) * 100:+.0f} pts (min +{g["beat_best_baseline_by"] * 100:.0f})'),
    ]


# ---------------- report ----------------
def pct(x):
    return "n/a" if x is None else f"{x:.1%}"


def write_report(path, args, cases, results, baselines, prov):
    gold_dist = Counter(c["gold"] for c in cases)
    L = [f"# Risk Classification Eval Report",
         f"- Run at: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
         f"- Provider/model: `{args.provider}` / `{args.model}`  |  runs per case: {args.runs}  |  temperature: {args.temperature}",
         f"- Cases: {len(cases)}  |  gold mix: {dict(gold_dist)}  |  rubric v1.0",
         f"- Provenance (sha256 prefixes): cases `{prov['cases_sha256']}`, run_eval.py `{prov['run_eval_sha256']}`, "
         f"prompts {prov['prompts']}",
         ""]
    if args.provider == "mock":
        L += ["> **MOCK RUN. Random outputs for plumbing tests. Do not cite any number below.**", ""]
    best = max(m["exact_acc"] for m in baselines.values())
    L += ["## Naive baselines (exact accuracy)", "| Baseline | Exact acc |", "|---|---|"]
    L += [f"| {k} | {pct(m['exact_acc'])} |" for k, m in baselines.items()] + [""]
    L += ["## Headline comparison", "| Metric | " + " | ".join(results) + " |", "|---|" + "---|" * len(results)]
    rows = [("Exact accuracy (runs)", "exact_acc"), ("Case-level accuracy (majority vote)", "case_level_acc"),
            ("Under-classification rate", "under_rate"), ("Over-classification rate", "over_rate"),
            ("Off-by-one rate", "off_by_one"), ("Critical under (High->Low), count", "critical_under"),
            ("Confidential recall", "conf_recall"), ("Injection resistance", "inj_exact"),
            ("Flip rate (cases)", "flip_rate"), ("Parse failures", "parse_fail")]
    for label, key in rows:
        vals = [results[v][0][key] for v in results]
        L.append(f"| {label} | " + " | ".join(str(x) if key == "critical_under" else pct(x) for x in vals) + " |")
    L.append("| Case-level 95% CI (Wilson) | " + " | ".join(
        f"{results[v][0]['case_ci'][0]:.0%} to {results[v][0]['case_ci'][1]:.0%}" for v in results) + " |")
    L.append("")
    for v, (m, fails) in results.items():
        L += [f"## {v}", "### Launch gate (pre-registered)", "| Criterion | Result | Verdict |", "|---|---|---|"]
        gc = gate_check(m, best)
        L += [f"| {a} | {b} | **{c}** |" for a, b, c in gc]
        verdict = "SHIP" if all(c in ("PASS", "n/a") for _, _, c in gc) else "DO NOT SHIP"
        L += ["", f"**Verdict for {v}: {verdict}**", "", "### Confusion matrix (rows = gold, columns = predicted, in runs)",
              "| Gold \\ Pred | Low | Medium | High | parse_fail |", "|---|---|---|---|---|"]
        for g in TIERS:
            c = m["confusion"][g]
            L.append(f"| {g} | {c['Low']} | {c['Medium']} | {c['High']} | {c['parse_fail']} |")
        L += ["", "### Accuracy by stratum (correct / runs)", "| Stratum | Correct | Runs |", "|---|---|---|"]
        L += [f"| {s} | {a} | {b} |" for s, (a, b) in m["per_stratum"].items()]
        L += ["", f"### Failures to feed the failure-mode catalog ({len(fails)} wrong runs; first 15)"]
        for f in fails[:15]:
            L += [f"- **{f['case_id']}** ({f['stratum']}): gold {f['gold']}, predicted {f['pred']}. "
                  f"Reasoning: {f['reasoning'][:260].strip()}"]
        L.append("")
    open(path, "w").write("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=list(PROVIDERS), default=None)
    ap.add_argument("--model", default="mock")
    ap.add_argument("--versions", nargs="+", default=list(DEFAULT_PROMPTS),
                    help="label=path.md pairs, or the default labels v1_baseline v2_enhanced")
    ap.add_argument("--selftest", action="store_true", help="check that prompts load cleanly, then exit")
    ap.add_argument("--dry-run", action="store_true", help="print the exact system prompt sent per version, then exit")
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--temperature", type=float, default=None, help="omit to match your production default")
    ap.add_argument("--cases", default="cases.jsonl")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--outdir", default="results")
    args = ap.parse_args()
    if not (args.selftest or args.dry_run) and not args.provider:
        ap.error("--provider is required (anthropic, openai, or mock)")
    if args.provider and args.provider != "mock" and args.model == "mock":
        ap.error("--model is required for real providers (use the model your prototype uses)")

    here = os.path.dirname(os.path.abspath(__file__))
    cases = [json.loads(l) for l in open(os.path.join(here, args.cases))]
    if args.selftest:
        selftest(here)
    prompts = parse_versions(args.versions, here)
    if args.dry_run:
        for v, system in prompts.items():
            print(f"===== {v} (sha256 {sha(system)}) =====\n{system}{SUFFIX}\n")
        raise SystemExit(0)
    jobs = []
    for v, system in prompts.items():
        jobs += [(v, system, c, k) for c in cases for k in range(args.runs)]
    with ThreadPoolExecutor(args.workers) as ex:
        raw = list(ex.map(lambda j: run_one(j, args.provider, args.model, args.temperature), jobs))

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out = os.path.join(here, args.outdir, stamp)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "raw.jsonl"), "w") as f:
        for r in raw:
            f.write(json.dumps(r) + "\n")

    cmap = {c["id"]: c for c in cases}
    results = {}
    for v in prompts:
        rows = [r for r in raw if r["version"] == v]
        fails = [{**r, "gold": cmap[r["case_id"]]["gold"], "stratum": cmap[r["case_id"]]["stratum"]}
                 for r in rows if r["pred"] != cmap[r["case_id"]]["gold"]]
        results[v] = (metrics(rows, cases), fails)
    baselines = {f"always {t}": metrics(baseline_rows(cases, t, args.runs), cases) for t in ["Medium", "High"]}
    prov = {"cases_sha256": sha(open(os.path.join(here, args.cases), encoding="utf-8").read()),
            "run_eval_sha256": sha(open(os.path.abspath(__file__), encoding="utf-8").read()),
            "prompts": {v: sha(t) for v, t in prompts.items()}}
    write_report(os.path.join(out, "report.md"), args, cases, results, baselines, prov)
    print(f"report: {os.path.join(out, 'report.md')}")


if __name__ == "__main__":
    main()
