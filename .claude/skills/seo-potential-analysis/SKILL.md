---
name: seo-potential-analysis
description: Quantify the traffic, lead, and ROI upside of an SEO engagement. Use when the user asks how much organic traffic or revenue is realistically achievable, wants a 12-month forecast, an SEA-equivalent value, or a click-delta projection. Applies the intent-aware Keyword Study 2026 CTR curve — never idealised textbook CTRs.
---

# SEO Potential Analysis

Run after a Status-Quo exists. Quantifies the **realistic upside**.

## Steps

1. Load the Status-Quo table for the domain.
2. Apply the **intent-aware CTR model** in `docs/ctr-model.md` (Keyword Study 2026:
   1.3M keywords, 94 domains). Classify intent first, then read the right curve.
   Pos 1 ≈ 5.59 % overall; navigational ≈ 8.9 %, informational ≈ 3.2 %.
   **Never** use the old Pos-1-=-28 % textbook table.
3. Set realistic 12-month target positions by current position × search volume:
   - >100 & SV >10k → Pos 15 · >100 & SV 5-10k → Pos 12
   - >100 & SV 1-5k → Pos 8 · >100 & SV <1k → Pos 5
   - already ranking → improve 1-10 positions
4. Compute Δ clicks per keyword; aggregate by cluster.
5. B2B leads: contact rate 1.5 / 2.5 / 3.5 %, close rate 10-20 %, deal value by industry.
6. SEA equivalence: `Δclicks × avg CPC` = ad-spend saved.
7. ROI: investment vs. (SEA value + lead value).

## Output

Save under `clients/<domain>/YYYY-MM-DD_Potential/`:
- `potential_<date>.xlsx` (per-keyword Δ + cluster rollup)
- `top20_delta.md`, `roi_scenarios.md` (conservative / realistic / optimistic)

Slash command: `/potenzial <domain>`. Methodology: `docs/workflows.md`.
