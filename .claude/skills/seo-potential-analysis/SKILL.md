---
name: seo-potential-analysis
description: Quantify the traffic, lead, and ROI upside of an SEO engagement. Use when the user asks how much organic traffic or revenue is realistically achievable, wants a 12-month forecast, an SEA-equivalent value, a click-delta projection, or a business case for SEO spend. Applies the intent-aware Keyword Study 2026 CTR curve — never idealised textbook CTRs.
---

# SEO Potential Analysis

Turn a Status-Quo into a **defensible business case**: how many extra clicks, leads,
and euros an SEO engagement realistically produces over 12 months.

## Preconditions

A Status-Quo table must exist for the domain (run `seo-status-quo` / `/status-quo`
first). You need, per keyword: search volume (SV), current position, current clicks,
impressions, and an intent label.

## Step 1 — Classify intent (this drives everything)

Each keyword is **transactional, commercial, informational, or navigational**. CTR at
the same position differs wildly by intent, so misclassifying inflates or deflates the
whole forecast. When unsure, infer from the SERP and the query form ("buy", "price",
"vs", "how to", brand name).

## Step 2 — Apply the intent-aware CTR curve

Read CTR from the **Keyword Study 2026** curve in [`docs/ctr-model.md`](../../docs/ctr-model.md)
(first-party GSC data, 1.3M keywords, 94 domains). Pick the column for the keyword's
intent, the row for its position. Anchor values at position 1:

| Intent | CTR @ Pos 1 |
|---|---|
| Navigational | ~8.9 % |
| Commercial | ~4.1 % |
| Transactional | ~3.7 % |
| Informational | ~3.2 % |
| Overall (blended) | ~5.6 % |

**Never** use the old textbook curve (Pos 1 = 28 %). Below position 20: ~0.3 % (21-50),
~0.1 % (50+).

## Step 3 — Set realistic 12-month target positions

| Current position | Search volume | Target |
|---|---|---|
| > 100 | > 10k | Pos 15 |
| > 100 | 5-10k | Pos 12 |
| > 100 | 1-5k | Pos 8 |
| > 100 | < 1k | Pos 5 |
| Already ranking | any | improve 1-10 positions by current strength |

Never promise Position 1 for a page sitting at 100+. Conservative targets keep the
offer credible.

## Step 4 — Compute the click delta

```
target_clicks  = SV × CTR(target_position, intent)
current_clicks = from GSC (or SV × CTR(current_position, intent) if missing)
delta_clicks   = max(0, target_clicks − current_clicks)
```

Aggregate `delta_clicks` by **cluster / theme** — per-keyword numbers are noisy; a
decision-maker acts on cluster rollups.

## Step 5 — Translate clicks into business value

- **Leads (B2B):** `leads = delta_clicks × contact_rate × close_rate`
  - contact rate: 1.5 % conservative / 2.5 % realistic / 3.5 % optimistic
  - close rate: 10-20 % (industry-specific)
  - revenue: `leads × average_deal_value`
- **SEA equivalence:** `delta_clicks × avg_CPC` = the ad spend this organic traffic
  would otherwise cost. Powerful framing for a SEA-heavy client.
- **ROI:** `(SEA_value + lead_revenue − investment) / investment`.

Run all three scenarios (conservative / realistic / optimistic) so the client sees a
range, not a single fragile number.

## Output

Save under `clients/<domain>/YYYY-MM-DD_Potential/`:
- `potential_<date>.xlsx` — per-keyword delta + cluster rollup
- `top20_delta.md` — Top 20 keywords by click-delta (the headline story)
- `roi_scenarios.md` — the three scenarios with the lead & SEA math

Slash command: `/potenzial <domain>`. Full methodology: `docs/workflows.md`.
