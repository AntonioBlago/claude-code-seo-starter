# SEO Potential Analysis — [CLIENT DOMAIN]

> **How to use this template.** This is the skeleton the `/visibly-seo-potential`
> command fills in. Replace every `[bracketed placeholder]`. Built **on top of the
> Status-Quo** — every current value comes from there / live GSC, every target from the
> matrix below. CTR comes from the **intent-aware Keyword Study 2026 curve**
> ([`docs/ctr-model.md`](../docs/ctr-model.md)) — **never** the inflated textbook curve.
> Order mirrors the business case: *what's realistic → how many extra clicks → what that's
> worth → at what ROI*.

| | |
|---|---|
| **Domain** | [example.com] |
| **Horizon** | 12 months |
| **Date** | [YYYY-MM-DD] |
| **Built on** | Status-Quo of [YYYY-MM-DD] |
| **CTR model** | Keyword Study 2026 (intent-aware, first-party GSC) |
| **Prepared by** | [Your name / agency] |

---

## 1. Executive summary

> 4–6 sentences. The upside as a range, never a single fragile number.

[Closing the ranking gap on the [N] priority keywords is worth ~[X] additional organic
clicks/month at the realistic target positions — roughly [Y] qualified leads/year and
~[€Z] in equivalent paid-search spend saved. Conservative to optimistic spans [€A]–[€B].
This puts a [ratio] return on a [investment] engagement. Methodology and per-keyword numbers below.]

---

## 2. Method — assumptions on the table

> State every lever up front. A forecast is only credible if the inputs are visible.

- **CTR curve:** Keyword Study 2026, intent-aware (Pos 1 ≈ 5.6 % blended; navigational ≈ 8.9 %,
  commercial ≈ 4.1 %, transactional ≈ 3.7 %, informational ≈ 3.2 %). Below pos 20: ~0.3 % (21–50), ~0.1 % (50+).
- **Target positions:** from the matrix in section 3 — never Position 1 for a page at 100+.
- **Lead model (B2B):** contact rate [1.5 % cons. / 2.5 % real. / 3.5 % opt.], close rate [10–20 %],
  average deal value [€…].
- **SEA equivalence:** average CPC [€…] (from [Visibly / Google Ads / estimate]).
- **Investment compared against:** [Year-1 offer total — fill once the offer exists].

---

## 3. Target-position matrix

> The rule that turns "currently ranks at X" into "realistically reaches Y in 12 months".
> Conservative targets keep the forecast defensible.

| Current position | Search volume | 12-month target |
|---|---|---|
| > 100 | > 10k | Pos 15 |
| > 100 | 5–10k | Pos 12 |
| > 100 | 1–5k | Pos 8 |
| > 100 | < 1k | Pos 5 |
| Already ranking | any | improve 1–10 positions by current strength |

---

## 4. Per-keyword delta

> One row per priority keyword. `target_clicks = SV × CTR(target, intent)`;
> `delta = max(0, target_clicks − current_clicks)`. Keep all rows in the Excel export;
> show the most important [N] here.

| Keyword | Intent | SV | Cur. pos | Cur. clicks | Target pos | Target CTR | Target clicks | Δ clicks |
|---|---|---|---|---|---|---|---|---|
| [keyword] | [trans/comm/info/nav] | [sv] | [pos] | [clk] | [pos] | [ctr %] | [clk] | [+Δ] |
| [keyword] | [...] | [sv] | [pos] | [clk] | [pos] | [ctr %] | [clk] | [+Δ] |
| … | | | | | | | | |

*Full table: `potential_<date>.xlsx`.*

---

## 5. Cluster rollup

> Per-keyword numbers are noisy; a decision-maker acts on **cluster** totals. Aggregate the
> deltas by theme.

| Cluster / theme | Keywords | Current clicks/mo | Target clicks/mo | Δ clicks/mo | Δ share |
|---|---|---|---|---|---|
| [cluster A] | [count] | [clk] | [clk] | [+Δ] | [%] |
| [cluster B] | [count] | [clk] | [clk] | [+Δ] | [%] |
| **Total** | [count] | [clk] | [clk] | **[+Δ]** | 100 % |

---

## 6. Top 20 by click-delta

> The headline story — the 20 keywords that move the most traffic. This is what goes on a slide.

| # | Keyword | Cluster | Cur. pos → target | Δ clicks/mo |
|---|---|---|---|---|
| 1 | [keyword] | [cluster] | [pos → pos] | [+Δ] |
| 2 | [keyword] | [cluster] | [pos → pos] | [+Δ] |
| … (to 20) | | | | |

---

## 7. Business value — three scenarios

> Run all three so the client sees a range. `leads = Δclicks × contact_rate × close_rate`;
> `revenue = leads × avg_deal_value`; `SEA_value = Δclicks × avg_CPC`.

| | Conservative | Realistic | Optimistic |
|---|---|---|---|
| Contact rate | 1.5 % | 2.5 % | 3.5 % |
| Additional clicks / month | [N] | [N] | [N] |
| Additional clicks / year | [N×12] | [N×12] | [N×12] |
| Qualified leads / year | [N] | [N] | [N] |
| Pipeline / revenue impact / year | [€] | [€] | [€] |
| Equivalent SEA spend saved / year | [€] | [€] | [€] |

---

## 8. ROI

> Tie value to investment. The number that justifies the engagement.

- **Total annual value (realistic):** SEA saved [€X] + lead revenue [€Y] = **[€X+Y]**
- **Investment (Year-1 offer):** [€I]
- **ROI:** `([€X+Y] − [€I]) / [€I]` = **[ratio / %]**
- **Payback:** [months to break even]

---

## 9. Next step

> Hand-off into the offer. One clear line.

[These numbers are the ROI backbone of the proposal. Run `/visibly-seo-offer [example.com]`
to turn this potential into a phased, priced engagement the client can say yes to.]
