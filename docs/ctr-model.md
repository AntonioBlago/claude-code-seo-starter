# The CTR model — Keyword Study 2026

A potential analysis lives or dies by its **click-through-rate curve**. Most SEO
templates still use the old idealised numbers (Position 1 = 28 %). In the real
world — post-AI-Overviews, post-zero-click — those are wildly optimistic, and an
offer built on them collapses the moment a client checks the math against their
own Search Console.

This blueprint uses the **Keyword Study 2026** by [Antonio Blago](https://antonioblago.de)
instead — CTR by position derived from **first-party Google Search Console data**.

> **Source of truth:** <https://www.antonioblago.com/keyword-study-2026-organic-search-ctr>
> **Sample:** 1,303,046 keywords across 94 domains · 2025-08-27 → 2026-02-23 · raw GSC, not clickstream estimates.
> The live page recomputes from current data — treat the numbers below as a snapshot and re-pull when you need the latest.

## Why this study is different: intent-aware curves

The headline insight isn't just "position 1 is ~5.6 %, not 28 %". It's that **CTR
depends on search intent**. A navigational keyword at position 1 earns more than
twice the CTR of an informational one. Forecasting with a single blended curve
quietly over- or under-states the upside depending on the keyword mix.

## The curve (CTR %, positions 1-20)

| Pos | Overall | Transactional | Commercial | Informational | Navigational |
|----:|--------:|--------------:|-----------:|--------------:|-------------:|
| 1 | 5.59 | 3.68 | 4.10 | 3.24 | 8.91 |
| 2 | 3.15 | 2.38 | 3.44 | 2.44 | 5.30 |
| 3 | 2.37 | 2.45 | 2.23 | 1.87 | 3.98 |
| 4 | 2.07 | 2.75 | 1.75 | 1.33 | 2.55 |
| 5 | 1.51 | 2.06 | 1.37 | 0.83 | 1.60 |
| 6 | 1.11 | 1.45 | 1.07 | 0.59 | 1.09 |
| 7 | 0.87 | 1.08 | 0.85 | 0.51 | 0.88 |
| 8 | 0.61 | 0.83 | 0.71 | 0.20 | 0.84 |
| 9 | 0.58 | 0.73 | 0.59 | 0.25 | 0.66 |
| 10 | 0.52 | 0.65 | 0.51 | 0.27 | 0.52 |
| 11 | 0.49 | 0.58 | 0.48 | 0.26 | 0.54 |
| 12 | 0.47 | 0.53 | 0.48 | 0.26 | 0.48 |
| 13 | 0.46 | 0.49 | 0.45 | 0.32 | 0.52 |
| 14 | 0.47 | 0.45 | 0.45 | 0.74 | 0.45 |
| 15 | 0.45 | 0.46 | 0.46 | 0.48 | 0.39 |
| 16 | 0.49 | 0.44 | 0.50 | 0.61 | 0.51 |
| 17 | 0.47 | 0.45 | 0.46 | 0.54 | 0.60 |
| 18 | 0.45 | 0.41 | 0.44 | 0.61 | 0.55 |
| 19 | 0.44 | 0.40 | 0.47 | 0.44 | 0.41 |
| 20 | 0.40 | 0.37 | 0.39 | 0.51 | 0.45 |

**Below position 20** (the study reports positions 1-20; extrapolate conservatively):

| Position range | CTR |
|---|---|
| 21-50 | 0.3 % |
| 50+ | 0.1 % |

## How it's applied

```python
# Keyword Study 2026 — CTR % by position, per search intent.
# Source: antonioblago.com/keyword-study-2026-organic-search-ctr
CTR_BY_INTENT = {
    # pos: (overall, transactional, commercial, informational, navigational)
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

def ctr_for(position: int, intent: str = "overall") -> float:
    """CTR as a fraction (e.g. 0.0559). intent: overall | transactional |
    commercial | informational | navigational."""
    idx = _INTENT_IDX[intent]
    pos = max(1, round(position))
    if pos <= 20:
        return CTR_BY_INTENT[pos][idx] / 100
    return (0.3 if pos <= 50 else 0.1) / 100

def projected_clicks(search_volume: int, position: int, intent: str = "overall") -> float:
    return search_volume * ctr_for(position, intent)

def click_delta(search_volume, current_pos, target_pos, intent="overall"):
    """Upside of moving a keyword from its current to its target position."""
    return (projected_clicks(search_volume, target_pos, intent)
            - projected_clicks(search_volume, current_pos, intent))
```

Classify each keyword's intent first (the Visibly AI MCP `classify_keywords` tool
does this), then forecast with the matching curve. Fall back to `overall` when
intent is unknown.

## Why honest, intent-aware inputs win

- **Defensible.** When a prospect cross-checks against their own GSC, your
  forecast holds up instead of looking inflated.
- **Accurate per cluster.** A transactional-heavy cluster and an informational
  one have very different ceilings — the intent curves capture that; a blended
  curve hides it.
- **Conservative by design.** Under-promise on clicks, then over-deliver. That's
  how you keep retainers.

> Have your own first-party data? Swap in your own curve — just keep it empirical
> and document the source.
