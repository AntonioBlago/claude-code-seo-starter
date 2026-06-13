"""
offer_economics — the money math behind a phased SEO offer.

Powers the `/visibly-seo-offer` skill. Takes the phase pricing you set in the
offer plus the realistic annual value from the Potential analysis and produces the
investment table, the ROI multiple and the payback period — the numbers section 8
of templates/offer-template.md needs.

    from claude_tools.offer_economics import pricing_table, business_case
    phases = [
        {"phase": "Phase 0 — Setup & data review", "investment": 2500},
        {"phase": "Phase 1 — Audit",               "investment": 6500},
        {"phase": "Phase 2 — Retainer (10 mo)",    "investment": 25000},
    ]
    bc = business_case(phases, annual_value=120000)
    # bc["year1_total"], bc["roi"], bc["roi_pct"], bc["payback_months"]

CLI:
    python -m claude_tools.offer_economics \
        --phases "Setup:2500,Audit:6500,Retainer:25000" \
        --annual-value 120000 --out offer_economics.xlsx
"""
from __future__ import annotations

import argparse

import pandas as pd


def pricing_table(phases) -> pd.DataFrame:
    """Phase rows + a Year-1 total row. `phases`: list of {phase, investment[, ...]}."""
    df = pd.DataFrame(phases)
    if "investment" not in df:
        raise KeyError("each phase needs an 'investment' value")
    total = float(df["investment"].sum())
    total_row = {c: "" for c in df.columns}
    total_row["phase"] = "Year-1 total"
    total_row["investment"] = total
    return pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)


def business_case(phases, annual_value: float) -> dict:
    """ROI multiple + payback from phase pricing and realistic annual value.

    roi      = (annual_value - year1_total) / year1_total   (a multiple, e.g. 2.33)
    payback  = months until cumulative monthly value covers the Year-1 spend.
    """
    table = pricing_table(phases)
    year1_total = float(table.iloc[-1]["investment"])
    monthly_value = annual_value / 12 if annual_value else 0.0
    roi = (annual_value - year1_total) / year1_total if year1_total else None
    payback = (year1_total / monthly_value) if monthly_value else None
    return {
        "pricing_table": table,
        "year1_total": round(year1_total),
        "annual_value": round(annual_value),
        "roi": round(roi, 2) if roi is not None else None,
        "roi_pct": f"{roi * 100:.0f} %" if roi is not None else "n/a",
        "value_multiple": f"{annual_value / year1_total:.1f}x" if year1_total else "n/a",
        "payback_months": round(payback, 1) if payback is not None else None,
    }


def summary_table(bc: dict) -> pd.DataFrame:
    """Section-8 ROI block as a 2-column table."""
    rows = [
        ("Total annual value (realistic)", f"{bc['annual_value']:,} €"),
        ("Investment (Year-1 offer)", f"{bc['year1_total']:,} €"),
        ("Value : cost", bc["value_multiple"]),
        ("ROI", bc["roi_pct"]),
        ("Payback", f"{bc['payback_months']} months" if bc["payback_months"] else "n/a"),
    ]
    return pd.DataFrame(rows, columns=["Metric", "Value"])


def to_excel(bc: dict, path: str) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as xl:
        bc["pricing_table"].to_excel(xl, sheet_name="Pricing", index=False)
        summary_table(bc).to_excel(xl, sheet_name="ROI", index=False)


def _parse_phases(arg: str):
    phases = []
    for part in arg.split(","):
        name, _, amount = part.rpartition(":")
        phases.append({"phase": name.strip() or part, "investment": float(amount)})
    return phases


def main(argv=None):
    ap = argparse.ArgumentParser(description="Phased pricing + ROI/payback for an SEO offer.")
    ap.add_argument("--phases", required=True,
                    help='comma-separated "Name:amount" pairs, e.g. "Setup:2500,Audit:6500"')
    ap.add_argument("--annual-value", type=float, required=True,
                    help="realistic annual value from the Potential analysis (€)")
    ap.add_argument("--out", help="optional .xlsx output")
    args = ap.parse_args(argv)

    bc = business_case(_parse_phases(args.phases), args.annual_value)
    print(summary_table(bc).to_string(index=False))
    if args.out:
        to_excel(bc, args.out)
        print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
