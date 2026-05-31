# Corporate Identity — [YOUR NAME / AGENCY]

> The single human-readable reference for your brand. Claude reads this when
> producing any client-facing document. Keep it in sync with `brand.py`
> (the machine-readable version). **Replace every bracketed placeholder.**

## Brand

- **Name:** [Your Name / Agency]
- **Title / role:** [e.g. SEO Freelancer]
- **Tagline:** [e.g. Neuro-SEO System®]
- **Website:** [https://example.com]
- **Email:** [you@example.com]
- **Phone:** [+00 000 000 000]

## Colours

| Role | Hex | RGB |
|---|---|---|
| **Primary (accent)** | `#f6571e` | 246, 87, 30 |
| Secondary | `#2f8ae5` | 47, 138, 229 |
| Dark (cover/footer) | `#0c1115` | 12, 17, 21 |
| Body text | `#171716` | 23, 23, 22 |
| Light gray (rows) | `#f8f8f8` | 248, 248, 248 |
| Success (KPI good) | `#1abc9c` | 26, 188, 156 |
| Warning (KPI) | `#ff912c` | 255, 145, 44 |
| Danger (KPI critical) | `#cf2e2e` | 207, 46, 46 |

## Fonts

- **Headings:** [e.g. Montserrat] — Regular, Bold, Italic
- **Body:** [e.g. Aptos / Mulish] — Regular, Bold
- TTF files live in `fonts/`. Always register with `uni=True` for accents and symbols.

## Document rules

- **Cover:** dark background, primary accent bar, white title, brand + client + date.
- **Header/footer:** dark bar + primary accent line; brand left, contact centred.
- **Section titles:** primary accent bar + bold heading font.
- **Tables:** primary header row (white text), alternating white / light-gray rows.
- **KPI/ROI boxes:** colour-coded (success / warning / danger) with a second non-colour cue.
- **Typography:** real accented characters (`für`, not `fuer`); real `® ™ ©` symbols.
- **Wide tables:** when a cell exceeds ~50 characters, switch to `multi_cell` layout.

## Do NOT commit to a public repo

This file is a **template**. Your filled-in version — and anything sensitive
(bank details, signatures, private contact data, logos under licence) — belongs in
a private location, never in the public starter. Keep secrets out of git.
