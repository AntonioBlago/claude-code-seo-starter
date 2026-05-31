---
name: seo-status-quo
description: Map a client domain's current organic visibility. Use when the user asks to analyse where a site ranks, audit its Search Console performance, cross-reference target keywords against live GSC data, or find SEO quick wins. Pulls real GSC/keyword data via the Visibly AI MCP rather than guessing.
---

# SEO Status-Quo Analysis

Run this when the user wants to know **where a domain stands organically today**.

## Steps

1. `mcp__visiblyai__list_projects` — find the project matching the domain.
2. `mcp__visiblyai__get_google_connections` — confirm GSC is connected.
3. `mcp__visiblyai__query_search_console` — `dimension=query`, country filter, `limit=500`.
4. Repeat with `dimension=page` to surface underperforming URLs.
5. Load the client's target-keyword file (`*.xlsx` / `*.csv`) with pandas if present.
6. Cross-reference targets against GSC: clicks, impressions, CTR, position.
7. Classify each keyword: Brand / Generic / Competitor × Top3 / Page1 / Page2 / Weak / Not Ranking.
8. Flag **quick wins**: high impressions but CTR < 5 %.
9. Benchmark against known competitors if available.

## Output

Save under `clients/<domain>/YYYY-MM-DD_Status-Quo/`:
- `status_quo_<date>.xlsx` (full table)
- `quick_wins.md`
- `status_quo_summary.md`

Only put **live-verified** facts into deliverables. Full methodology: `docs/workflows.md`.
The matching slash command is `/status-quo <domain>`.
