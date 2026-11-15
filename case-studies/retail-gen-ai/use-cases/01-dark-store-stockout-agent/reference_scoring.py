#!/usr/bin/env python3
"""Python reference for stockoutScoring.ts. Same logic, same rounding, same operation order.

    python reference_scoring.py            # run golden tests + print expected outputs for mock_skus.json
    python reference_scoring.py --write    # regenerate expected_outputs.json

The app's numbers must match expected_outputs.json exactly. POLICY values are placeholder
assumptions for the fictional store; change them here and in stockoutScoring.ts together.
"""
import json, math, os, re, sys

P = dict(OPERATING_HOURS=16, REVIEW_DAYS=1, SAFETY_DAYS=1, ESCALATE_BELOW=60, MIN_HISTORY_DAYS=7,
         FULL_HISTORY_DAYS=28, CV_VOLATILE=0.35, STALE_MINUTES=60, PROMO_PENALTY=10, STALE_PENALTY=15)
RANK = {"high": 0, "medium": 1, "low": 2, "unknown": 3, "none": 4}


def half(x): return math.floor(x + 0.5)
def round1(x): return math.floor(x * 10 + 0.5) / 10
def mean(xs): return sum(xs) / len(xs)
def pstdev(xs):
    m = mean(xs)
    return math.sqrt(sum((x - m) * (x - m) for x in xs) / len(xs))


def assess(s):
    sales = s["daily_sales"][-P["FULL_HISTORY_DAYS"]:]
    n = len(sales)
    base = dict(hours_to_stockout=None, days_of_cover=None, velocity_used=None, velocity_change_pct=None,
                reorder_qty=None, confidence_pct=0, escalated=True)
    if n < P["MIN_HISTORY_DAYS"]:
        return {**base, "risk_level": "unknown", "confidence_drivers": ["short_history"], "reason": "insufficient_history"}
    v7, v3 = mean(sales[-7:]), mean(sales[-3:])
    v = max(v7, v3) if s["promo_active"] else v7
    if v <= 0:
        return {**base, "risk_level": "unknown", "velocity_used": 0, "confidence_drivers": ["no_recent_sales"],
                "reason": "no_recent_sales"}
    cover = s["on_hand"] / v
    L = s["lead_time_days"]
    horizon = L + P["REVIEW_DAYS"] + P["SAFETY_DAYS"]
    risk = "high" if cover < L else "medium" if cover < L + P["REVIEW_DAYS"] else "low" if cover < horizon else "none"
    wow = None
    if n >= 14:
        prev = mean(sales[-14:-7])
        if prev > 0:
            wow = half((v7 / prev - 1) * 100)
    m = mean(sales)
    cv = pstdev(sales) / m if m > 0 else 1
    drivers, conf = [], 100 * (1 - min(cv, 1))
    if cv >= P["CV_VOLATILE"]: drivers.append("volatile_demand")
    if s["promo_active"]: conf -= P["PROMO_PENALTY"]; drivers.append("promo_active")
    if s["data_age_minutes"] > P["STALE_MINUTES"]: conf -= P["STALE_PENALTY"]; drivers.append("stale_data")
    if n < P["FULL_HISTORY_DAYS"]: conf -= P["FULL_HISTORY_DAYS"] - n; drivers.append("short_history")
    cp = max(0, min(100, half(conf)))
    esc = cp < P["ESCALATE_BELOW"]
    qty = max(0, math.ceil(v * horizon - s["on_hand"] - s["on_order"] - 1e-9))
    return dict(risk_level=risk, hours_to_stockout=half(cover * P["OPERATING_HOURS"]), days_of_cover=round1(cover),
                velocity_used=round1(v), velocity_change_pct=wow, reorder_qty=None if esc else qty,
                confidence_pct=cp, escalated=esc, confidence_drivers=drivers, reason=None)


def sort_key(a): return (RANK[a["risk_level"]], a["hours_to_stockout"] if a["hours_to_stockout"] is not None else 1e9)


def allowed_numbers(s, a):
    xs = [a["hours_to_stockout"], a["days_of_cover"], a["velocity_used"], a["velocity_change_pct"], a["reorder_qty"],
          a["confidence_pct"], s["on_hand"], s["on_order"], s["lead_time_days"], s["data_age_minutes"]]
    return [abs(x) for x in xs if x is not None]


def grounding_check(text, allowed):
    toks = [float(t) for t in re.findall(r"\d+(?:\.\d+)?", text)]
    bad = [t for t in toks if not any(abs(a - t) <= 0.05 for a in allowed)]
    return len(bad) == 0, bad


def sku(**kw):
    d = dict(id="t", name="Test", category="x", on_hand=0, on_order=0, lead_time_days=1, promo_active=False,
             data_age_minutes=10, daily_sales=[10] * 28)
    d.update(kw)
    return d


GOLDEN = [
    ("steady, plenty of cover", sku(on_hand=120), dict(risk_level="none", hours_to_stockout=192, confidence_pct=100, reorder_qty=0)),
    ("stocks out before restock", sku(on_hand=8), dict(risk_level="high", hours_to_stockout=13, reorder_qty=22, confidence_pct=100)),
    ("exactly at lead time is medium, not high", sku(on_hand=10), dict(risk_level="medium", days_of_cover=1.0)),
    ("inbound order reduces quantity", sku(on_hand=8, on_order=15), dict(reorder_qty=7)),
    ("promo uses the higher 3-day velocity", sku(on_hand=40, promo_active=True, daily_sales=[10] * 25 + [20, 20, 20]),
     dict(velocity_used=20.0, risk_level="low", confidence_drivers=["promo_active"])),
    ("stale data lowers confidence by 15", sku(data_age_minutes=95), dict(confidence_pct=85, confidence_drivers=["stale_data"])),
    ("low confidence withholds the quantity", sku(on_hand=8, daily_sales=[2, 40] * 14),
     dict(escalated=True, reorder_qty=None)),
    ("zero recent sales", sku(daily_sales=[0] * 28), dict(risk_level="unknown", escalated=True, reorder_qty=None)),
    ("too little history", sku(daily_sales=[5, 6, 5]), dict(risk_level="unknown", confidence_pct=0)),
    ("week-over-week change", sku(daily_sales=[10] * 21 + [14] * 7), dict(velocity_change_pct=40)),
]


def run_golden():
    bad = 0
    for name, s, exp in GOLDEN:
        out = assess(s)
        diff = {k: (out[k], v) for k, v in exp.items() if out[k] != v}
        print(("PASS " if not diff else "FAIL ") + name + ("" if not diff else f"  {diff}"))
        bad += bool(diff)
    ok, bad_nums = grounding_check("Stock lasts about 13 hours; reorder 22 units.", allowed_numbers(*(lambda s: (s, assess(s)))(sku(on_hand=8))))
    ok2, _ = grounding_check("Stock lasts about 14 hours.", allowed_numbers(*(lambda s: (s, assess(s)))(sku(on_hand=8))))
    print("PASS grounding accepts matching numbers" if ok else "FAIL grounding accepts matching numbers")
    print("PASS grounding rejects a wrong number" if not ok2 else "FAIL grounding rejects a wrong number")
    return bad + (not ok) + ok2


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    fails = run_golden()
    skus = json.load(open(os.path.join(here, "mock_skus.json"))) if os.path.exists(os.path.join(here, "mock_skus.json")) else []
    rows = [{"id": s["id"], "name": s["name"], **assess(s)} for s in skus]
    rows.sort(key=sort_key)
    for r in rows:
        print(f'{r["name"]:<28}{r["risk_level"]:<8}{str(r["hours_to_stockout"]):>5} h  conf {r["confidence_pct"]:>3}%  '
              f'qty {str(r["reorder_qty"]):>5}  wow {str(r["velocity_change_pct"]):>5}  esc {r["escalated"]}')
    if "--write" in sys.argv:
        json.dump(rows, open(os.path.join(here, "expected_outputs.json"), "w"), indent=1)
        print("wrote expected_outputs.json")
    raise SystemExit(1 if fails else 0)
