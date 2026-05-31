---
description: SEO Status-Quo analysis for a client — GSC + keyword cross-reference + quick wins
argument-hint: <client-domain>
---

Run **Workflow 1 — SEO Status-Quo Analysis** (see `docs/workflows.md`) for client `$ARGUMENTS`.

## Inputs

- Client folder: `./clients/$ARGUMENTS/` (create if missing)
- Keyword files: look for `*.xlsx`, `*.csv` in the client folder
- GSC: via Visibly AI MCP (`list_projects` → match domain → `query_search_console`)

## Steps

1. `mcp__visiblyai__list_projects` — find the project matching `$ARGUMENTS`
2. `mcp__visiblyai__get_google_connections` — confirm GSC is wired
3. `mcp__visiblyai__query_search_console` with country filter, `dimension=query`, `limit=500`
4. Repeat with `dimension=page` for underperforming URLs
5. Read the client keyword Excel/CSV (pandas):
   ```bash
   python -c "import pandas as pd; print(pd.read_excel('clients/$ARGUMENTS/keywords.xlsx').head())"
   ```
6. Cross-reference target keywords against GSC (clicks, impressions, CTR, position)
7. Classify: Brand / Generic / Competitor × Top3 / Page1 / Page2 / Weak / Not Ranking
8. Flag Quick Wins: high impressions, CTR < 5 %
9. Competitor benchmark (if competitors are known for this client)

## Output

Save to `./clients/$ARGUMENTS/YYYY-MM-DD_Status-Quo/`:
- `status_quo_<YYYY-MM-DD>.xlsx` (full table)
- `quick_wins.md` (actionable list)
- `status_quo_summary.md` (executive summary)

Use today's date for the folder and filename.
