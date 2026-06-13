"""
ctr_model — the Keyword Study 2026 CTR curve, as importable code.

Single source of truth (in Python) for the click-through-rate model documented in
`docs/ctr-model.md`. Intent-aware, derived from first-party Google Search Console
data (1.3M keywords, 94 domains). NEVER use the old idealised curve (Pos 1 = 28 %).

    Source: https://www.antonioblago.com/keyword-study-2026-organic-search-ctr

Usage:
    from claude_tools.ctr_model import ctr_for, projected_clicks, click_delta, target_position
    ctr_for(3, "commercial")            # -> 0.0223
    projected_clicks(2000, 5, "transactional")
    target_position(current_pos=120, search_volume=8000)   # -> 12
"""
from __future__ import annotations

# CTR % by position, per search intent. Keep in sync with docs/ctr-model.md.
# pos: (overall, transactional, commercial, informational, navigational)
CTR_BY_INTENT = {
    1:  (5.59, 3.68, 4.10, 3.24, 8.91),  2:  (3.15, 2.38, 3.44, 2.44, 5.30),
    3:  (2.37, 2.45, 2.23, 1.87, 3.98),  4:  (2.07, 2.75, 1.75, 1.33, 2.55),
    5:  (1.51, 2.06, 1.37, 0.83, 1.60),  6:  (1.11, 1.45, 1.07, 0.59, 1.09),
    7:  (0.87, 1.08, 0.85, 0.51, 0.88),  8:  (0.61, 0.83, 0.71, 0.20, 0.84),
    9:  (0.58, 0.73, 0.59, 0.25, 0.66),  10: (0.52, 0.65, 0.51, 0.27, 0.52),
    11: (0.49, 0.58, 0.48, 0.26, 0.54),  12: (0.47, 0.53, 0.48, 0.26, 0.48),
    13: (0.46, 0.49, 0.45, 0.32, 0.52),  14: (0.47, 0.45, 0.45, 0.74, 0.45),
    15: (0.45, 0.46, 0.46, 0.48, 0.39),  16: (0.49, 0.44, 0.50, 0.61, 0.51),
    17: (0.47, 0.45, 0.46, 0.54, 0.60),  18: (0.45, 0.41, 0.44, 0.61, 0.55),
    19: (0.44, 0.40, 0.47, 0.44, 0.41),  20: (0.40, 0.37, 0.39, 0.51, 0.45),
}
_INTENT_IDX = {"overall": 0, "transactional": 1, "commercial": 2,
               "informational": 3, "navigational": 4}

# Synonyms accepted from keyword files / MCP output, normalised to the keys above.
_INTENT_ALIASES = {
    "transactional": "transactional", "transaction": "transactional", "buy": "transactional",
    "commercial": "commercial", "commercial investigation": "commercial", "comparison": "commercial",
    "informational": "informational", "information": "informational", "info": "informational",
    "navigational": "navigational", "navigation": "navigational", "brand": "navigational",
    "overall": "overall", "blended": "overall", "mixed": "overall", "": "overall",
}


def normalize_intent(intent: str | None) -> str:
    """Map a free-form intent label onto one of the five curve columns."""
    if intent is None:
        return "overall"
    return _INTENT_ALIASES.get(str(intent).strip().lower(), "overall")


def ctr_for(position: float, intent: str = "overall") -> float:
    """CTR as a fraction (e.g. 0.0559) for a position + intent.

    Positions 1-20 read from the study; 21-50 -> 0.3 %, 50+ -> 0.1 %
    (extrapolated below the position-20 floor the study reports)."""
    idx = _INTENT_IDX[normalize_intent(intent)]
    pos = max(1, round(position))
    if pos <= 20:
        return CTR_BY_INTENT[pos][idx] / 100
    return (0.3 if pos <= 50 else 0.1) / 100


def projected_clicks(search_volume: float, position: float, intent: str = "overall") -> float:
    """Monthly clicks a keyword would earn at a given position."""
    return float(search_volume) * ctr_for(position, intent)


def click_delta(search_volume: float, current_pos: float, target_pos: float,
                intent: str = "overall", current_clicks: float | None = None) -> float:
    """Upside (>= 0) of moving a keyword from current to target position.

    Pass measured `current_clicks` (from GSC) when available — more accurate than
    modelling the current position with the curve."""
    base = current_clicks if current_clicks is not None else projected_clicks(
        search_volume, current_pos, intent)
    return max(0.0, projected_clicks(search_volume, target_pos, intent) - base)


def target_position(current_pos: float, search_volume: float) -> int:
    """Realistic 12-month target position (the matrix from CLAUDE.md / docs).

    Not-ranking / page-3+ (pos > 100, treat <=0 / missing as 'not ranking'):
        SV > 10k -> 15 · 5-10k -> 12 · 1-5k -> 8 · < 1k -> 5
    Already ranking (pos <= 100): improve by current strength, never below 1,
    never worse than now. A heuristic the analyst can override per keyword."""
    pos = current_pos if (current_pos and current_pos > 0) else 1000
    sv = search_volume or 0
    if pos > 100:
        if sv > 10000:
            return 15
        if sv >= 5000:
            return 12
        if sv >= 1000:
            return 8
        return 5
    # Already ranking: bigger jumps from deeper positions, finer near the top.
    if pos > 50:
        improve = 10
    elif pos > 20:
        improve = 7
    elif pos > 10:
        improve = 5
    elif pos > 3:
        improve = 3
    else:
        improve = 1
    return max(1, round(pos) - improve)


if __name__ == "__main__":
    # Quick self-check / reference print.
    print("CTR @ pos 1 by intent:")
    for name in _INTENT_IDX:
        print(f"  {name:14s} {ctr_for(1, name) * 100:5.2f} %")
    print("\ntarget_position examples:")
    for cp, sv in [(120, 12000), (120, 6000), (120, 2000), (120, 500), (45, 3000), (8, 3000)]:
        print(f"  pos {cp:>4}  SV {sv:>6}  -> Pos {target_position(cp, sv)}")
