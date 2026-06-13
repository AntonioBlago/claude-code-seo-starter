"""
io_utils — shared helpers for reading client data and resolving messy columns.

Keyword exports and GSC dumps never agree on column names ("Keyword" vs "query"
vs "Suchbegriff"; "SV" vs "Search Volume" vs "Suchvolumen"). These helpers find
the right column by a list of candidates so the data modules don't each re-invent
it. Used by status_quo.py and potential.py.
"""
from __future__ import annotations

import re
from typing import Iterable

import pandas as pd

# Candidate header names per logical field (lower-cased, punctuation-stripped).
COLUMN_ALIASES = {
    "keyword": ["keyword", "query", "suchbegriff", "term", "keywords", "search term"],
    "search_volume": ["sv", "search volume", "searchvolume", "suchvolumen", "volume",
                      "avg monthly searches", "monthly searches", "vol"],
    "position": ["position", "pos", "avg position", "average position", "rank",
                 "ranking", "current position", "durchschnittliche position"],
    "clicks": ["clicks", "klicks", "click", "url clicks"],
    "impressions": ["impressions", "impr", "impr.", "impressionen", "impression"],
    "ctr": ["ctr", "click through rate", "click-through rate"],
    "intent": ["intent", "search intent", "suchintention", "intention"],
    "cluster": ["cluster", "theme", "topic", "thema", "group", "gruppe", "category",
                "kategorie", "page type"],
    "url": ["url", "page", "landing page", "address", "seite", "top pages"],
}


def _canon(name: str) -> str:
    """Lower-case, collapse whitespace/punctuation for tolerant header matching."""
    return re.sub(r"[^a-z0-9]+", " ", str(name).lower()).strip()


def find_col(df: pd.DataFrame, field: str, required: bool = False) -> str | None:
    """Return the actual column name in `df` matching a logical `field`.

    `field` is a key of COLUMN_ALIASES (e.g. "search_volume") or a raw candidate."""
    candidates = COLUMN_ALIASES.get(field, [field])
    canon_map = {_canon(c): c for c in df.columns}
    for cand in candidates:
        hit = canon_map.get(_canon(cand))
        if hit is not None:
            return hit
    # Substring fallback: "Search Volume (avg)" still matches "search volume".
    for cand in candidates:
        cc = _canon(cand)
        for canon_col, real in canon_map.items():
            if cc in canon_col:
                return real
    if required:
        raise KeyError(
            f"Could not find a '{field}' column. Looked for {candidates}; "
            f"available columns: {list(df.columns)}")
    return None


def load_table(path: str) -> pd.DataFrame:
    """Read a keyword/GSC export (.xlsx/.xls/.csv/.tsv) into a DataFrame."""
    p = str(path).lower()
    if p.endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    sep = "\t" if p.endswith(".tsv") else None  # None -> sniff , or ;
    return pd.read_csv(path, sep=sep, engine="python")


def to_number(series: pd.Series) -> pd.Series:
    """Coerce a column to numeric, tolerating '1,234', '12%', '1.5k' style values."""
    def parse(v):
        if pd.isna(v):
            return None
        s = str(v).strip().replace("%", "").replace(" ", "")
        mult = 1
        if s and s[-1].lower() == "k":
            mult, s = 1000, s[:-1]
        # 1.234,56 (de) vs 1,234.56 (en): if both separators, the last is decimal.
        if "," in s and "." in s:
            s = s.replace(",", "") if s.rfind(".") > s.rfind(",") else s.replace(".", "").replace(",", ".")
        elif "," in s:
            s = s.replace(",", ".") if s.count(",") == 1 else s.replace(",", "")
        try:
            return float(s) * mult
        except ValueError:
            return None
    return series.map(parse)


def norm_key(series: pd.Series) -> pd.Series:
    """Normalise keyword text for joining (lower, trim, collapse spaces)."""
    return series.astype(str).map(lambda s: re.sub(r"\s+", " ", s.strip().lower()))


def pick(values: Iterable, default=None):
    """First non-null value from an iterable, else default."""
    for v in values:
        if v is not None and not (isinstance(v, float) and pd.isna(v)):
            return v
    return default
