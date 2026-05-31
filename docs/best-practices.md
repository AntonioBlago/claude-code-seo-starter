# Best practices — lessons from real SEO engagements

Hard-won patterns from running this workflow across client projects. Steal them.

## Data & verification

- **Verify before you claim.** Before stating any technical fact (canonical,
  hreflang, robots.txt, indexability, redirects), confirm it live. Only confirmed
  facts go into a client deliverable. A wrong claim in a PDF costs trust you can't
  buy back.
- **Prefer first-party data.** Visibly AI MCP → real GSC/GA numbers beat any
  third-party estimate. Use estimates only to fill genuine gaps, and label them.
- **Cross-reference, don't assume.** Map the client's target keyword list against
  live GSC data. The gap between "keywords they care about" and "keywords they
  actually rank for" is where the strategy lives.

## Analysis

- **Use the empirical, intent-aware CTR curve** ([`ctr-model.md`](ctr-model.md)).
  Never the textbook Pos-1-=-28 % numbers. Classify intent first, then forecast.
- **Set realistic 12-month targets.** Don't promise Position 1 for a page sitting
  at 100+. Target Pos 5-15 depending on current position and search volume.
- **Aggregate to clusters.** Per-keyword deltas are noisy; cluster-level rollups
  are what a decision-maker can act on.
- **Always show the ROI bridge.** Tie additional clicks → leads → revenue, and to
  equivalent SEA spend saved. Numbers in tables, prose around them.

## Crawling

- **Rate-limit aggressive crawls.** On hardened or CDN-fronted shops (e.g.
  Shopify behind Cloudflare), uncapped crawls get 429/403'd. Throttle request rate
  and concurrency, or use a proper scraping API. A polite crawler finishes; a
  greedy one gets blocked.

## Client deliverables

- **Be specific and actionable.** "Add 10 internal links from these 5 pages to
  /target" beats "improve internal linking". Always give priority + estimated
  effort per recommendation.
- **Recognise existing work.** Read prior audits before producing anything. Show
  the client their previous analyses are integrated, not duplicated — it's the
  difference between a partner and a vendor.
- **Use real accented characters.** `für`, not `fuer`. `ä ö ü ß é ñ`, never ASCII
  substitutes. Register PDF fonts with `uni=True`.
- **Use real symbols.** `®` `™` `©`, never `(R)` / `(TM)` / `(C)`.

## PDF generation

- **Centralise your CI.** Put colours and fonts in one module; don't copy-paste
  them into every script.
- **Break wide tables.** When cell text exceeds ~50 characters, switch from a
  simple table to manual `multi_cell` layout so cells stay readable.
- **Verify the rendered output.** Open the PDF, check the cover, fonts, accents,
  and page breaks before handing it over. Never ship a broken PDF.

## Working with Claude Code

- **Let the hook steer tool choice.** The `seo-check.sh` hook nudges Claude to
  Visibly AI MCP on SEO-intent prompts — keep extending its keyword triggers.
- **One folder per client, dated task subfolders.** Never a flat file dump.
- **Keep secrets and client data out of git.** `.env` and `clients/` are
  gitignored for a reason.
