# SEO Status-Quo — [CLIENT DOMAIN]

> **How to use this template.** This is the skeleton the `/visibly-seo-status-quo`
> command fills in. Replace every `[bracketed placeholder]`. **Every number here must
> come from live data** (GSC via the Visibly AI MCP + the client's keyword file) — never
> estimate. Order mirrors how the analysis reads: *where do we stand → what does each
> keyword do → where are the fast wins → who's beating us*.

| | |
|---|---|
| **Domain** | [example.com] |
| **Target market** | [country / language — the GSC country filter you used] |
| **Date** | [YYYY-MM-DD] |
| **Data sources** | GSC ([date range]), keyword file ([N] keywords), [competitors if used] |
| **Prepared by** | [Your name / agency] |

---

## 1. Executive summary

> 4–6 sentences a decision-maker reads in 30 seconds. The honest picture, not a sales pitch.

[Of the [M] target keywords, the domain ranks for [N] ([X] in the top 10, [Y] on page 2,
[Z] not ranking). The biggest gap is [one finding]. There are [K] quick wins — keywords
already earning impressions but losing the click — worth ~[estimate] additional clicks/month
with on-page work alone. Full numbers below; this is the baseline every later phase builds on.]

---

## 2. Visibility at a glance

> The headline counts. Fill from the cross-referenced table in section 4.

| Metric | Value |
|---|---|
| Target keywords tracked | [M] |
| Ranking (any position) | [N] ([N/M %]) |
| Top 3 | [count] |
| Page 1 (pos 4–10) | [count] |
| Page 2 (pos 11–20) | [count] |
| Weak (pos 21–50) | [count] |
| Not ranking (50+ / none) | [count] |
| Total organic clicks / month (target set) | [from GSC] |
| Total impressions / month (target set) | [from GSC] |
| Blended CTR | [clicks / impressions] |

---

## 3. Keyword classification

> Two axes: **type** (Brand · Generic · Competitor) and **ranking bucket**. The split tells
> you how much visibility is brand-defensive vs. genuine generic demand capture.

| Type | Keywords | Clicks | Impressions | Share of clicks |
|---|---|---|---|---|
| Brand | [count] | [clicks] | [impr] | [%] |
| Generic | [count] | [clicks] | [impr] | [%] |
| Competitor | [count] | [clicks] | [impr] | [%] |

> A high brand share with low generic share = the site converts demand it *already owns*
> but isn't winning new demand. That's the strategic story.

---

## 4. Status-Quo table (cross-referenced)

> The core deliverable. One row per target keyword, GSC values mapped on. In the Excel
> export keep all rows; in this summary show the most important [N] (e.g. by impressions or
> business value). **Live GSC values only.**

| Keyword | SV | Position | Clicks | Impr. | CTR | Type | Bucket | Quick win? |
|---|---|---|---|---|---|---|---|---|
| [keyword] | [sv] | [pos] | [clk] | [impr] | [ctr %] | [Brand/Generic/Competitor] | [Top3/Page1/Page2/Weak/NotRanking] | [✓ / —] |
| [keyword] | [sv] | [pos] | [clk] | [impr] | [ctr %] | [...] | [...] | [...] |
| … | | | | | | | | |

*Full table: `status_quo_<date>.xlsx`.*

---

## 5. Underperforming pages

> From the `dimension=page` GSC pull: URLs with impressions but weak clicks. These are
> intent-mismatch / on-page candidates — demand is reaching them, the page isn't closing it.

| URL | Impressions | Clicks | CTR | Avg. position | Likely issue |
|---|---|---|---|---|---|
| [/url] | [impr] | [clk] | [ctr %] | [pos] | [title/meta · intent mismatch · thin content] |
| … | | | | | |

---

## 6. Quick wins

> A quick win = **high impressions + CTR below ~5 % + position in the 4–15 striking-distance
> band**. Demand and partial visibility already exist; you close a gap, you don't create one.
> Give the specific lever per keyword — vague wins don't get done.

| # | Keyword / page | Position | Impr. | CTR | Lever | Est. effort |
|---|---|---|---|---|---|---|
| 1 | [keyword] | [pos] | [impr] | [ctr %] | [rewrite title+meta / add internal links / expand section] | [S/M/L] |
| 2 | [keyword] | [pos] | [impr] | [ctr %] | [specific action] | [S/M/L] |
| 3 | … | | | | | |

---

## 7. Competitor benchmark *(optional)*

> Only if competitors are known for this client. Compare positions on **shared** keywords —
> show where the client is out-ranked and by whom.

| Keyword | [Client] | [Competitor A] | [Competitor B] | Gap |
|---|---|---|---|---|
| [keyword] | [pos] | [pos] | [pos] | [+/- positions] |
| … | | | | |

---

## 8. What this means — next step

> Hand-off line into the Potential analysis. One or two sentences, no fluff.

[The ranking gap on [N] generic keywords plus the [K] quick wins are the raw material for a
12-month forecast. Run `/visibly-seo-potential [example.com]` to quantify the click, lead and
revenue upside.]
