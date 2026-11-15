// src/lib/stockoutScoring.ts
// Deterministic stockout scoring for NovaMart Express (fictional). NO AI in this file.
// Policy values are placeholder assumptions for a fictional store.

export type Risk = "none" | "low" | "medium" | "high" | "unknown";

export interface SkuInput {
  id: string;
  name: string;
  category: string;
  on_hand: number;
  on_order: number;
  lead_time_days: number;
  promo_active: boolean;
  data_age_minutes: number;
  daily_sales: number[]; // units/day, oldest first, up to 28 values
}

export interface Assessment {
  risk_level: Risk;
  hours_to_stockout: number | null; // operating hours, integer
  days_of_cover: number | null; // 1 decimal
  velocity_used: number | null; // units/day, 1 decimal
  velocity_change_pct: number | null; // last 7 days vs previous 7 days, integer percent
  reorder_qty: number | null; // null when escalated or insufficient data
  confidence_pct: number; // 0-100 integer; a data-reliability heuristic, NOT a calibrated probability
  escalated: boolean;
  confidence_drivers: string[]; // codes, no numbers
  reason: string | null; // set when data is insufficient
}

export const POLICY = {
  OPERATING_HOURS: 16,
  REVIEW_DAYS: 1,
  SAFETY_DAYS: 1,
  ESCALATE_BELOW: 60,
  MIN_HISTORY_DAYS: 7,
  FULL_HISTORY_DAYS: 28,
  CV_VOLATILE: 0.35,
  STALE_MINUTES: 60,
  PROMO_PENALTY: 10,
  STALE_PENALTY: 15,
};

const half = (x: number) => Math.floor(x + 0.5); // same rounding in every language
const round1 = (x: number) => Math.floor(x * 10 + 0.5) / 10;
const mean = (xs: number[]) => xs.reduce((a, b) => a + b, 0) / xs.length;
const pstdev = (xs: number[]) => {
  const m = mean(xs);
  return Math.sqrt(xs.reduce((a, b) => a + (b - m) * (b - m), 0) / xs.length);
};

export function assess(s: SkuInput): Assessment {
  const P = POLICY;
  const sales = s.daily_sales.slice(-P.FULL_HISTORY_DAYS);
  const n = sales.length;
  if (n < P.MIN_HISTORY_DAYS) {
    return { risk_level: "unknown", hours_to_stockout: null, days_of_cover: null, velocity_used: null,
      velocity_change_pct: null, reorder_qty: null, confidence_pct: 0, escalated: true,
      confidence_drivers: ["short_history"], reason: "insufficient_history" };
  }
  const v7 = mean(sales.slice(-7));
  const v3 = mean(sales.slice(-3));
  const v = s.promo_active ? Math.max(v7, v3) : v7;
  if (v <= 0) {
    return { risk_level: "unknown", hours_to_stockout: null, days_of_cover: null, velocity_used: 0,
      velocity_change_pct: null, reorder_qty: null, confidence_pct: 0, escalated: true,
      confidence_drivers: ["no_recent_sales"], reason: "no_recent_sales" };
  }
  const cover = s.on_hand / v;
  const L = s.lead_time_days;
  const horizon = L + P.REVIEW_DAYS + P.SAFETY_DAYS;
  const risk: Risk = cover < L ? "high" : cover < L + P.REVIEW_DAYS ? "medium" : cover < horizon ? "low" : "none";

  let wow: number | null = null;
  if (n >= 14) {
    const prev = mean(sales.slice(-14, -7));
    if (prev > 0) wow = half((v7 / prev - 1) * 100);
  }

  const m = mean(sales);
  const cv = m > 0 ? pstdev(sales) / m : 1;
  const drivers: string[] = [];
  let conf = 100 * (1 - Math.min(cv, 1));
  if (cv >= P.CV_VOLATILE) drivers.push("volatile_demand");
  if (s.promo_active) { conf -= P.PROMO_PENALTY; drivers.push("promo_active"); }
  if (s.data_age_minutes > P.STALE_MINUTES) { conf -= P.STALE_PENALTY; drivers.push("stale_data"); }
  if (n < P.FULL_HISTORY_DAYS) { conf -= P.FULL_HISTORY_DAYS - n; drivers.push("short_history"); }
  const confidence_pct = Math.max(0, Math.min(100, half(conf)));
  const escalated = confidence_pct < P.ESCALATE_BELOW;

  const qty = Math.max(0, Math.ceil(v * horizon - s.on_hand - s.on_order - 1e-9));
  return {
    risk_level: risk,
    hours_to_stockout: half(cover * P.OPERATING_HOURS),
    days_of_cover: round1(cover),
    velocity_used: round1(v),
    velocity_change_pct: wow,
    reorder_qty: escalated ? null : qty,
    confidence_pct,
    escalated,
    confidence_drivers: drivers,
    reason: null,
  };
}

const RISK_RANK: Record<Risk, number> = { high: 0, medium: 1, low: 2, unknown: 3, none: 4 };
export function compareUrgency(a: Assessment, b: Assessment): number {
  const r = RISK_RANK[a.risk_level] - RISK_RANK[b.risk_level];
  if (r !== 0) return r;
  return (a.hours_to_stockout ?? 1e9) - (b.hours_to_stockout ?? 1e9);
}

// Numbers the AI rationale is allowed to cite (everything shown in the panel, plus the item's own inputs).
export function allowedNumbers(s: SkuInput, a: Assessment): number[] {
  const xs = [a.hours_to_stockout, a.days_of_cover, a.velocity_used, a.velocity_change_pct,
    a.reorder_qty, a.confidence_pct, s.on_hand, s.on_order, s.lead_time_days, s.data_age_minutes];
  return xs.filter((x): x is number => x !== null).map((x) => Math.abs(x));
}

// Grounding check: every numeric token in the rationale must match an allowed number.
export function groundingCheck(rationale: string, allowed: number[]): { ok: boolean; offending: number[] } {
  const tokens = (rationale.match(/\d+(?:\.\d+)?/g) ?? []).map(Number);
  const offending = tokens.filter((t) => !allowed.some((a) => Math.abs(a - t) <= 0.05));
  return { ok: offending.length === 0, offending };
}

// Deterministic fallback sentence. Never labelled as AI output.
export function templateRationale(s: SkuInput, a: Assessment): string {
  if (a.risk_level === "unknown") {
    return `${s.name}: not enough recent sales history to assess stockout risk. Escalated to the Supply Chain Planner.`;
  }
  const promo = s.promo_active ? " A promotion is active." : "";
  const tail = a.escalated
    ? ` Signal confidence is ${a.confidence_pct}%, below the ${POLICY.ESCALATE_BELOW}% threshold, so this is escalated to the Supply Chain Planner.`
    : ` Recommended reorder: ${a.reorder_qty} units.`;
  return `${s.name}: about ${a.hours_to_stockout} operating hours of stock left against a ${s.lead_time_days}-day supplier lead time; recent sales average ${a.velocity_used} units a day.${promo}${tail}`;
}
