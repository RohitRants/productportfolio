#!/usr/bin/env python3
"""Generate mock_skus.json (synthetic raw inputs only; no outputs). Deterministic."""
import json, random
from reference_scoring import assess

WEEK = [1.0, 0.95, 0.95, 1.0, 1.1, 1.35, 1.25]  # weekday pattern, day 0 = oldest


def series(rng, base, noise, spike_last3=1.0, surge_last7=1.0, n=28):
    out = []
    for d in range(n):
        v = base * WEEK[d % 7] * (1 + rng.uniform(-noise, noise))
        if d >= n - 7: v *= surge_last7
        if d >= n - 3: v *= spike_last3
        out.append(max(0, round(v)))
    return out


def build():
    rng = random.Random(11)
    # name, category, base, noise, spike3, surge7, lead, promo, age_min, target_cover_days, on_order, history_days
    spec = [
        ("Full Cream Milk 1L", "Dairy", 40, 0.08, 1.0, 1.4, 1, False, 12, 0.45, 0, 28),
        ("Sandwich Bread", "Bakery", 30, 0.08, 1.0, 1.0, 1, False, 8, 1.4, 0, 28),
        ("Instant Noodles 5-Pack", "Pantry", 28, 0.45, 1.6, 1.0, 1, True, 95, 0.6, 0, 28),
        ("Cola 750ml", "Beverages", 25, 0.10, 1.0, 1.0, 2, False, 15, 3.6, 0, 28),
        ("Potato Chips 150g", "Snacks", 18, 0.12, 1.0, 1.0, 2, False, 20, 9.0, 0, 28),
        ("Eggs 12-Pack", "Dairy", 22, 0.07, 1.0, 1.0, 1, False, 6, 0.7, 0, 28),
        ("Bottled Water 1L", "Beverages", 35, 0.06, 1.0, 1.0, 1, False, 10, 8.0, 0, 28),
        ("Bananas 1kg", "Produce", 15, 0.12, 1.0, 1.0, 1, False, 14, 2.3, 0, 28),
        ("Greek Yogurt 400g (new listing)", "Dairy", 9, 0.20, 1.0, 1.0, 2, False, 9, 2.0, 0, 5),
        ("Orange Juice 1L", "Beverages", 12, 0.15, 1.0, 1.0, 2, False, 18, 2.4, 6, 28),
    ]
    skus = []
    for i, (name, cat, base, noise, sp, su, lead, promo, age, cover, onord, hist) in enumerate(spec, 1):
        sales = series(rng, base, noise, sp, su)[-hist:]
        s = dict(id=f"SKU-{i:03d}", name=name, category=cat, on_hand=0, on_order=onord, lead_time_days=lead,
                 promo_active=promo, data_age_minutes=age, daily_sales=sales)
        v7 = sum(sales[-7:]) / 7
        v3 = sum(sales[-3:]) / 3
        v = max(v7, v3) if promo else v7
        s["on_hand"] = max(1, round(cover * v))
        skus.append(s)
    return skus


if __name__ == "__main__":
    json.dump(build(), open("mock_skus.json", "w"))
    print("wrote mock_skus.json")
