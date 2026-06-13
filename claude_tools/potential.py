"""
potential — turn a Status-Quo into a defensible 12-month business case.

Powers the `/visibly-seo-potential` skill. Takes the Status-Quo table (keywords
with SV, current position, current clicks, intent, cluster) and:

  * sets a realistic target position per keyword (ctr_model.target_position),
  * computes target clicks via the intent-aware Keyword Study 2026 CTR curve,
  * derives the click delta (measured current clicks preferred over modelled),
  * rolls deltas up by cluster,
  * runs conservative / realistic / optimistic lead, SEA & ROI scenarios,
  * writes a multi-sheet xlsx matching templates/potential-template.md.

CLI:
    python -m claude_tools.potential \
        --in clients/example.com/2026-06-13_Status-Quo/status_quo_2026-06-13.xlsx \
        --out clients/example.com/2026-06-13_Potential/potential_2026-06-13.xlsx \
        --avg-cpc 3.50 --close-rate 0.15 --deal-value 8000 --investment 36000

NEVER uses idealised textbook CTRs — only ctr_model (docs/ctr-model.md).
"""
from __future__ import annotations

import argparse

import pandas as pd

from . import ctr_model
from .io_utils import find_col, load_table, to_number

# Lead-model defaults (CLAUDE.md workflow 2 / templates/potential-template.md).
CONTACT_RATES = {"conservative": 0.015, "realistic": 0.025, "optimistic": 0.035}
DEFAULT_CLOSE_RATE = 0.15


def build_deltas(df: pd.DataFrame, *, sv_col=None, pos_col=None, clicks_col=None,
                 intent_col=None, cluster_col=None,
                 target_override: dict | None = None) -> pd.DataFrame:
    """Add Intent, Target pos, Target CTR, Target/Current clicks and Δ clicks per keyword."""
    kw_col = find_col(df, "keyword", required=True)
    sv_col = sv_col or find_col(df, "search_volume", required=True)
    pos_col = pos_col or find_col(df, "position")
    clicks_col = clicks_col or find_col(df, "clicks")
    intent_col = intent_col or find_col(df, "intent")
    cluster_col = cluster_col or find_col(df, "cluster")

    out = pd.DataFrame()
    out["Keyword"] = df[kw_col]
    out["Cluster"] = df[cluster_col] if cluster_col else "(uncategorised)"
    out["Intent"] = (df[intent_col].map(ctr_model.normalize_intent)
                     if intent_col else "overall")
    out["SV"] = to_number(df[sv_col]).fillna(0)
    out["Cur. pos"] = to_number(df[pos_col]) if pos_col else None
    out["Cur. clicks"] = to_number(df[clicks_col]) if clicks_col else None

    def target(row):
        if target_override and row["Keyword"] in target_override:
            return int(target_override[row["Keyword"]])
        return ctr_model.target_position(row["Cur. pos"], row["SV"])

    out["Target pos"] = out.apply(target, axis=1)
    out["Target CTR"] = out.apply(
        lambda r: ctr_model.ctr_for(r["Target pos"], r["Intent"]), axis=1)
    out["Target clicks"] = (out["SV"] * out["Target CTR"]).round(0)

    def cur_clicks(r):
        if r["Cur. clicks"] is not None and not pd.isna(r["Cur. clicks"]):
            return r["Cur. clicks"]
        if r["Cur. pos"] and not pd.isna(r["Cur. pos"]):
            return ctr_model.projected_clicks(r["SV"], r["Cur. pos"], r["Intent"])
        return 0.0

    out["Cur. clicks"] = out.apply(cur_clicks, axis=1).round(0)
    out["Δ clicks"] = (out["Target clicks"] - out["Cur. clicks"]).clip(lower=0)
    return out.sort_values("Δ clicks", ascending=False).reset_index(drop=True)


def cluster_rollup(deltas: pd.DataFrame) -> pd.DataFrame:
    """Aggregate deltas by cluster, with each cluster's share of total upside."""
    g = (deltas.groupby("Cluster", dropna=False)
         .agg(Keywords=("Keyword", "count"),
              **{"Current clicks/mo": ("Cur. clicks", "sum"),
                 "Target clicks/mo": ("Target clicks", "sum"),
                 "Δ clicks/mo": ("Δ clicks", "sum")})
         .reset_index())
    total = g["Δ clicks/mo"].sum()
    g["Δ share"] = (g["Δ clicks/mo"] / total).fillna(0) if total else 0.0
    g = g.sort_values("Δ clicks/mo", ascending=False).reset_index(drop=True)
    grand = pd.DataFrame([{
        "Cluster": "Total", "Keywords": g["Keywords"].sum(),
        "Current clicks/mo": g["Current clicks/mo"].sum(),
        "Target clicks/mo": g["Target clicks/mo"].sum(),
        "Δ clicks/mo": total, "Δ share": 1.0,
    }])
    return pd.concat([g, grand], ignore_index=True)


def value_scenarios(total_delta_clicks: float, *, avg_cpc=0.0, close_rate=DEFAULT_CLOSE_RATE,
                    deal_value=0.0, investment=0.0,
                    contact_rates=CONTACT_RATES) -> pd.DataFrame:
    """Conservative/realistic/optimistic leads, revenue, SEA value and ROI per year."""
    rows = []
    annual_clicks = total_delta_clicks * 12
    for name, contact in contact_rates.items():
        leads = annual_clicks * contact * close_rate
        revenue = leads * deal_value
        sea = annual_clicks * avg_cpc
        value = revenue + sea
        roi = (value - investment) / investment if investment else None
        rows.append({
            "Scenario": name.capitalize(),
            "Contact rate": f"{contact * 100:.1f} %",
            "Δ clicks/mo": round(total_delta_clicks),
            "Δ clicks/yr": round(annual_clicks),
            "Leads/yr": round(leads, 1),
            "Revenue/yr €": round(revenue),
            "SEA saved/yr €": round(sea),
            "Total value/yr €": round(value),
            "ROI": f"{roi * 100:.0f} %" if roi is not None else "n/a (set --investment)",
        })
    return pd.DataFrame(rows)


def to_excel(deltas: pd.DataFrame, rollup: pd.DataFrame, scenarios: pd.DataFrame,
             path: str) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as xl:
        deltas.to_excel(xl, sheet_name="Per-keyword delta", index=False)
        deltas.head(20).to_excel(xl, sheet_name="Top 20 by delta", index=False)
        rollup.to_excel(xl, sheet_name="Cluster rollup", index=False)
        scenarios.to_excel(xl, sheet_name="Value scenarios", index=False)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Status-Quo -> 12-month potential & ROI xlsx.")
    ap.add_argument("--in", dest="inp", required=True, help="Status-Quo file (.xlsx/.csv)")
    ap.add_argument("--out", required=True, help="output .xlsx path")
    ap.add_argument("--avg-cpc", type=float, default=0.0, help="average CPC for SEA equivalence (€)")
    ap.add_argument("--close-rate", type=float, default=DEFAULT_CLOSE_RATE, help="lead close rate (0-1)")
    ap.add_argument("--deal-value", type=float, default=0.0, help="average deal value (€)")
    ap.add_argument("--investment", type=float, default=0.0, help="Year-1 offer total for ROI (€)")
    ap.add_argument("--sheet", default=0, help="sheet name/index when reading an xlsx")
    args = ap.parse_args(argv)

    p = args.inp.lower()
    if p.endswith((".xlsx", ".xls")):
        sheet = int(args.sheet) if str(args.sheet).isdigit() else args.sheet
        df = pd.read_excel(args.inp, sheet_name=sheet)
    else:
        df = load_table(args.inp)

    deltas = build_deltas(df)
    rollup = cluster_rollup(deltas)
    scenarios = value_scenarios(
        deltas["Δ clicks"].sum(), avg_cpc=args.avg_cpc, close_rate=args.close_rate,
        deal_value=args.deal_value, investment=args.investment)
    to_excel(deltas, rollup, scenarios, args.out)

    print(f"Wrote {args.out}")
    print(f"  {len(deltas)} keywords · +{round(deltas['Δ clicks'].sum())} clicks/mo "
          f"(+{round(deltas['Δ clicks'].sum() * 12)}/yr)")
    real = scenarios[scenarios['Scenario'] == 'Realistic'].iloc[0]
    print(f"  realistic: {real['Leads/yr']} leads/yr · "
          f"{real['Total value/yr €']:,} € value · ROI {real['ROI']}")


if __name__ == "__main__":
    main()
