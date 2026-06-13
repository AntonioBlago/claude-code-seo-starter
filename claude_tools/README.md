# claude_tools — Python engine behind the SEO skills

Reusable, importable modules that do the **deterministic number-crunching and PDF
rendering** the four `visibly-seo-*` skills rely on. The skills (and Claude) gather the
data via the Visibly AI MCP; these modules turn it into the exact tables, deltas, ROI
math and client-ready PDFs the markdown templates expect — the same way every time, with
nothing invented.

> **Single sources of truth.** The CTR curve lives in [`docs/ctr-model.md`](../docs/ctr-model.md)
> (mirrored into [`ctr_model.py`](ctr_model.py)); the brand/CI lives in
> [`templates/ci/brand.py`](../templates/ci/brand.py) (imported by [`ci_pdf.py`](ci_pdf.py)).
> Change them there, not in copies.

## Setup (once)

Creates a dedicated `claude_tools_venv/` (Python 3.12 preferred) and installs the deps.

```powershell
# Windows / PowerShell
.\claude_tools\setup.ps1
```
```bash
# macOS / Linux / Git-Bash
bash claude_tools/setup.sh
```

Then run any module as `-m claude_tools.<module>`:

```powershell
.\claude_tools_venv\Scripts\python.exe -m claude_tools.ctr_model      # self-check
```

`claude_tools_venv/` is gitignored — it's a local build, recreate it anywhere with the
setup script.

## Modules

| Module | Powers | What it does |
|---|---|---|
| [`ctr_model.py`](ctr_model.py) | potential | Intent-aware Keyword Study 2026 CTR curve; `ctr_for`, `projected_clicks`, `click_delta`, `target_position`. Never the idealised textbook curve. |
| [`io_utils.py`](io_utils.py) | status-quo, potential | Load xlsx/csv, auto-detect German/English columns, clean messy numbers (`1.234`, `12 %`, `1,5k`). |
| [`status_quo.py`](status_quo.py) | `/visibly-seo-status-quo` | Cross-reference target keywords × live GSC → Type + Ranking bucket + Quick-win flag → 3-sheet xlsx. |
| [`potential.py`](potential.py) | `/visibly-seo-potential` | Status-Quo → target positions → click deltas → cluster rollup → conservative/realistic/optimistic lead·SEA·ROI → 4-sheet xlsx. |
| [`offer_economics.py`](offer_economics.py) | `/visibly-seo-offer` | Phase pricing → Year-1 total, ROI multiple, payback months → ROI sheet for the offer. |
| [`ci_pdf.py`](ci_pdf.py) | `/visibly-seo-pdf-build` | Reusable `CIPDF` class (imports `brand.py`): cover, header/footer, section bars, wrapping tables, KPI/ROI boxes. Helvetica fallback if brand fonts absent. |

## Typical end-to-end run

```powershell
$py = ".\claude_tools_venv\Scripts\python.exe"

# 1) Status-Quo: keywords × GSC export (both pulled/saved by the skill)
& $py -m claude_tools.status_quo `
    --keywords "clients/example.com/_knowledge/keywords.xlsx" `
    --gsc      "clients/example.com/2026-06-13_Status-Quo/gsc_query.csv" `
    --brand-terms example --competitor-terms rockwool,isover `
    --out      "clients/example.com/2026-06-13_Status-Quo/status_quo_2026-06-13.xlsx"

# 2) Potential: the Status-Quo xlsx -> 12-month business case
& $py -m claude_tools.potential `
    --in  "clients/example.com/2026-06-13_Status-Quo/status_quo_2026-06-13.xlsx" `
    --out "clients/example.com/2026-06-13_Potential/potential_2026-06-13.xlsx" `
    --avg-cpc 3.50 --close-rate 0.15 --deal-value 8000 --investment 36000

# 3) Offer economics: phase pricing + ROI/payback
& $py -m claude_tools.offer_economics `
    --phases "Setup:2500,Audit:6500,Retainer:25000" `
    --annual-value 120000 --out "clients/example.com/2026-06-13_Offer/economics.xlsx"

# 4) PDF demo (verify CI renders on this machine)
& $py -m claude_tools.ci_pdf
```

Use modules from your own scripts too — `from claude_tools.ci_pdf import CIPDF`, etc.

## Design notes

- **No invented numbers.** Every output traces to an input cell or the documented CTR
  curve. Missing current clicks are modelled from position × CTR, and that's the only
  modelled value.
- **Column auto-detection** (`io_utils.COLUMN_ALIASES`) accepts both German and English
  headers (`Keyword`/`Suchbegriff`, `Suchvolumen`/`Search Volume`, `Position`/`Pos`, …).
  Override per-run with the `--*-col` flags where provided.
- **Templates match.** Output columns line up 1:1 with `templates/status-quo-template.md`
  and `templates/potential-template.md` so results drop straight into the deliverable.
