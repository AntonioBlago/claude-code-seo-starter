---
name: seo-status-quo
description: Map a client domain's current organic visibility. Use when the user asks to analyse where a site ranks, audit its Search Console performance, cross-reference target keywords against live GSC data, find quick wins, or benchmark against competitors. Pulls real GSC/keyword data via the Visibly AI MCP rather than guessing.
---

# SEO Status-Quo Analysis

Establish, with **live data only**, where a domain stands organically in a target
market today. This is the foundation every later phase builds on — so every fact here
must be verified, not assumed.

## Step 1 — Discover what's wired

1. `mcp__visiblyai__list_projects` — find the project matching the domain.
2. `mcp__visiblyai__get_google_connections` — confirm Search Console (and GA) are connected.

If no project/connection exists, stop and tell the user what to connect first.

## Step 2 — Pull live GSC performance

3. `mcp__visiblyai__query_search_console` — `dimension=query`, target-**country** filter,
   `limit=500`. This is the ground truth: clicks, impressions, CTR, average position.
4. Repeat with `dimension=page` to find URLs with impressions but weak clicks
   (underperforming pages = on-page/intent-mismatch candidates).

## Step 3 — Load the client's target keywords

5. Read the client's keyword file (`*.xlsx` / `*.csv`) with pandas. These are the
   keywords the *business* cares about — often different from what it actually ranks for.
   That gap is where the strategy lives.

## Step 4 — Cross-reference and classify

6. Map each target keyword onto the live GSC row (clicks, impressions, CTR, position).
7. Classify on two axes:
   - **Type:** Brand · Generic · Competitor
   - **Ranking bucket:** Top 3 · Page 1 (4-10) · Page 2 (11-20) · Weak (21-50) · Not Ranking (50+/none)

## Step 5 — Flag quick wins

8. A **quick win** = high impressions + CTR below ~5 % + position in the 4-15 "striking
   distance" band. These convert fastest: the demand and partial visibility already
   exist; you're closing a gap, not creating one. List them explicitly with the lever
   (title/meta, on-page, internal links).

## Step 6 — Competitor benchmark

9. `mcp__visiblyai__get_competitors` and `mcp__visiblyai__get_keywords` to compare
   positions on shared keywords. Show where the client is out-ranked and by whom.

## Output

Fill in the ready skeleton at [`templates/status-quo-template.md`](../../../templates/status-quo-template.md) —
it already has the visibility counts, classification split, cross-referenced keyword table,
underperforming pages, quick wins and competitor benchmark. Save under
`clients/<domain>/YYYY-MM-DD_Status-Quo/`:
- `status_quo_<date>.md` — summary (copied from the template)
- `status_quo_<date>.xlsx` — full cross-referenced table (all rows)
- `quick_wins.md` — prioritised, actionable (specific lever per keyword)

**Only live-verified facts** go into any deliverable. Slash command: `/visibly-seo-status-quo <domain>`.
Methodology: `docs/workflows.md`.
