---
description: Potential analysis — empirical CTR model + realistic targets + lead/ROI calculation
argument-hint: <client-domain>
---

Run **Workflow 2 — Potential Analysis** (see `docs/workflows.md`) for client `$ARGUMENTS`.

## Preconditions

- Status-Quo output must exist under `./clients/$ARGUMENTS/`. If it does not, stop
  and tell the user to run `/visibly-seo-status-quo $ARGUMENTS` first.

## Steps

1. Load the Status-Quo table (xlsx):
   ```bash
   python -c "import pandas as pd; df = pd.read_excel('clients/$ARGUMENTS/.../status_quo.xlsx'); print(df.columns.tolist())"
   ```
2. Apply the **empirical CTR model** from [`docs/ctr-model.md`](../../docs/ctr-model.md).
   Pos 1 ≈ 5.59 %, Pos 2 ≈ 3.15 %, Pos 3 ≈ 2.37 % … (real-world, not idealised).
   **Never** use the old textbook curve (Pos 1 = 28 %).
3. Set realistic 12-month target positions based on current position + search volume:
   - Currently > 100, SV > 10k → target Pos 15
   - Currently > 100, SV 5-10k → target Pos 12
   - Currently > 100, SV 1-5k → target Pos 8
   - Currently > 100, SV < 1k → target Pos 5
   - Already ranking → improve 1-10 positions depending on current
4. Compute Δ clicks per keyword and aggregate by cluster/theme.
5. B2B lead calc: contact rate 1.5 % / 2.5 % / 3.5 %, close rate 10-20 %,
   industry-specific deal value.
6. SEA equivalence: `Δclicks × avg CPC` → ad-spend saved.
7. ROI: investment vs. (SEA value + lead value).

## Output

Save to `./clients/$ARGUMENTS/YYYY-MM-DD_Potential/`:
- `potential_<YYYY-MM-DD>.xlsx` (per-keyword Δ + cluster rollup)
- `top20_delta.md` (Top 20 keywords by click-delta)
- `roi_scenarios.md` (conservative / realistic / optimistic)
