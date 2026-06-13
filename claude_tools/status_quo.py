"""
status_quo — turn a keyword file + live GSC data into the Status-Quo deliverable.

Powers the `/visibly-seo-status-quo` skill. The skill pulls GSC via the Visibly AI
MCP (query + page dimensions), saves it as CSV/XLSX, then runs this to:

  * cross-reference every target keyword against its live GSC row,
  * classify each by TYPE (Brand / Generic / Competitor) and RANKING BUCKET,
  * flag QUICK WINS (high impressions, CTR below threshold, striking-distance pos),
  * write a multi-sheet xlsx matching templates/status-quo-template.md.

CLI:
    python -m claude_tools.status_quo \
        --keywords clients/example.com/_knowledge/keywords.xlsx \
        --gsc clients/example.com/2026-06-13_Status-Quo/gsc_query.csv \
        --brand-terms example,examplegmbh \
        --competitor-terms rockwool,isover \
        --out clients/example.com/2026-06-13_Status-Quo/status_quo_2026-06-13.xlsx

All numbers come from the inputs — nothing is invented. Columns are auto-detected
(see io_utils.COLUMN_ALIASES); pass --keyword-col etc. to override.
"""
from __future__ import annotations

import argparse

import pandas as pd

from .io_utils import find_col, load_table, norm_key, to_number

# Quick-win defaults (see templates/status-quo-template.md section 6).
QW_MIN_IMPRESSIONS = 100
QW_MAX_CTR = 0.05          # below ~5 %
QW_POS_LOW, QW_POS_HIGH = 4, 15   # striking-distance band


def ranking_bucket(position) -> str:
    """Map an average position onto the five status-quo buckets."""
    if position is None or pd.isna(position) or position <= 0 or position > 100:
        return "Not Ranking"
    p = float(position)
    if p <= 3:
        return "Top 3"
    if p <= 10:
        return "Page 1"
    if p <= 20:
        return "Page 2"
    if p <= 50:
        return "Weak"
    return "Not Ranking"


def classify_type(keyword: str, brand_terms, competitor_terms) -> str:
    """Brand if it contains a brand term, Competitor if a competitor term, else Generic.
    Brand wins ties (brand+competitor in one query is still brand-defensive)."""
    k = str(keyword).lower()
    if any(t and t.lower() in k for t in brand_terms):
        return "Brand"
    if any(t and t.lower() in k for t in competitor_terms):
        return "Competitor"
    return "Generic"


def crossref(keywords_df: pd.DataFrame, gsc_df: pd.DataFrame,
             brand_terms=(), competitor_terms=(),
             keyword_col=None, sv_col=None) -> pd.DataFrame:
    """Join target keywords onto live GSC rows; add type + bucket + quick-win flag."""
    kw_col = keyword_col or find_col(keywords_df, "keyword", required=True)
    g_kw = find_col(gsc_df, "keyword", required=True)

    kw = keywords_df.copy()
    kw["_key"] = norm_key(kw[kw_col])
    sv = sv_col or find_col(kw, "search_volume")

    g = gsc_df.copy()
    g["_key"] = norm_key(g[g_kw])
    g_clicks = find_col(g, "clicks")
    g_impr = find_col(g, "impressions")
    g_pos = find_col(g, "position")
    g_ctr = find_col(g, "ctr")

    keep = {"_key": "_key"}
    if g_clicks: keep[g_clicks] = "Clicks"
    if g_impr: keep[g_impr] = "Impr."
    if g_pos: keep[g_pos] = "Position"
    if g_ctr: keep[g_ctr] = "CTR"
    g_small = g[list(keep)].rename(columns=keep)
    # One GSC row per keyword (sum clicks/impr, best position) in case of dupes.
    agg = {}
    if "Clicks" in g_small: agg["Clicks"] = "sum"
    if "Impr." in g_small: agg["Impr."] = "sum"
    if "Position" in g_small: agg["Position"] = "min"
    if "CTR" in g_small: agg["CTR"] = "mean"
    if agg:
        g_small = g_small.groupby("_key", as_index=False).agg(agg)

    out = kw.merge(g_small, on="_key", how="left")

    out["Keyword"] = out[kw_col]
    out["SV"] = to_number(out[sv]) if sv else None
    for c in ("Clicks", "Impr.", "Position"):
        if c in out:
            out[c] = to_number(out[c])
    # CTR: prefer GSC's, else derive from clicks/impr.
    if "CTR" in out:
        out["CTR"] = to_number(out["CTR"])
        # GSC CTR may arrive as 4.2 (percent) or 0.042 (fraction) — normalise to fraction.
        out.loc[out["CTR"] > 1, "CTR"] = out["CTR"] / 100
    if "CTR" not in out or out["CTR"].isna().all():
        if "Clicks" in out and "Impr." in out:
            out["CTR"] = (out["Clicks"] / out["Impr."]).where(out["Impr."] > 0)

    out["Type"] = out["Keyword"].map(
        lambda k: classify_type(k, brand_terms, competitor_terms))
    out["Bucket"] = out["Position"].map(ranking_bucket) if "Position" in out else "Not Ranking"
    out["Quick win?"] = _quick_win_flag(out)

    cols = ["Keyword", "SV", "Position", "Clicks", "Impr.", "CTR", "Type", "Bucket", "Quick win?"]
    return out[[c for c in cols if c in out]].sort_values(
        by=[c for c in ("Impr.", "Clicks") if c in out], ascending=False, na_position="last"
    ).reset_index(drop=True)


def _quick_win_flag(df: pd.DataFrame) -> pd.Series:
    if not {"Impr.", "CTR", "Position"} <= set(df.columns):
        return pd.Series(["—"] * len(df), index=df.index)
    cond = (
        (df["Impr."].fillna(0) >= QW_MIN_IMPRESSIONS)
        & (df["CTR"].fillna(1) < QW_MAX_CTR)
        & (df["Position"].between(QW_POS_LOW, QW_POS_HIGH))
    )
    return cond.map({True: "✓", False: "—"})


def quick_wins(df: pd.DataFrame) -> pd.DataFrame:
    """The quick-win rows only, biggest impressions first (= the priority order)."""
    if "Quick win?" not in df:
        return df.iloc[0:0]
    qw = df[df["Quick win?"] == "✓"].copy()
    if "Impr." in qw:
        qw = qw.sort_values("Impr.", ascending=False)
    return qw.reset_index(drop=True)


def visibility_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Section-2 headline counts for the template."""
    n = len(df)
    bucket = df["Bucket"].value_counts() if "Bucket" in df else pd.Series(dtype=int)
    ranking = int(n - bucket.get("Not Ranking", 0))
    clicks = float(df["Clicks"].sum()) if "Clicks" in df else 0.0
    impr = float(df["Impr."].sum()) if "Impr." in df else 0.0
    rows = [
        ("Target keywords tracked", n),
        ("Ranking (any position)", f"{ranking} ({ranking / n * 100:.0f} %)" if n else "0"),
        ("Top 3", int(bucket.get("Top 3", 0))),
        ("Page 1 (pos 4-10)", int(bucket.get("Page 1", 0))),
        ("Page 2 (pos 11-20)", int(bucket.get("Page 2", 0))),
        ("Weak (pos 21-50)", int(bucket.get("Weak", 0))),
        ("Not ranking (50+/none)", int(bucket.get("Not Ranking", 0))),
        ("Total clicks / month", round(clicks)),
        ("Total impressions / month", round(impr)),
        ("Blended CTR", f"{clicks / impr * 100:.2f} %" if impr else "n/a"),
        ("Quick wins", int((df["Quick win?"] == "✓").sum()) if "Quick win?" in df else 0),
    ]
    return pd.DataFrame(rows, columns=["Metric", "Value"])


def to_excel(df: pd.DataFrame, path: str) -> None:
    """Write Status-Quo, Quick wins and Summary sheets."""
    with pd.ExcelWriter(path, engine="openpyxl") as xl:
        df.to_excel(xl, sheet_name="Status-Quo", index=False)
        quick_wins(df).to_excel(xl, sheet_name="Quick wins", index=False)
        visibility_summary(df).to_excel(xl, sheet_name="Summary", index=False)


def _split(arg: str | None):
    return [t.strip() for t in arg.split(",")] if arg else []


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cross-reference keywords x GSC into a Status-Quo xlsx.")
    ap.add_argument("--keywords", required=True, help="client keyword file (.xlsx/.csv)")
    ap.add_argument("--gsc", required=True, help="GSC export, dimension=query (.csv/.xlsx)")
    ap.add_argument("--out", required=True, help="output .xlsx path")
    ap.add_argument("--brand-terms", help="comma-separated brand terms")
    ap.add_argument("--competitor-terms", help="comma-separated competitor terms")
    ap.add_argument("--keyword-col", help="override keyword column name in the keyword file")
    ap.add_argument("--sv-col", help="override search-volume column name")
    args = ap.parse_args(argv)

    kw = load_table(args.keywords)
    gsc = load_table(args.gsc)
    df = crossref(kw, gsc, _split(args.brand_terms), _split(args.competitor_terms),
                  keyword_col=args.keyword_col, sv_col=args.sv_col)
    to_excel(df, args.out)

    s = visibility_summary(df).set_index("Metric")["Value"]
    print(f"Wrote {args.out}")
    print(f"  {len(df)} keywords · ranking: {s['Ranking (any position)']} · "
          f"quick wins: {s['Quick wins']}")


if __name__ == "__main__":
    main()
