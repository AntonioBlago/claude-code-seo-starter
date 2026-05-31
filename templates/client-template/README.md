# Client folder template

Copy this whole folder to `clients/<domain.tld>/` for every new client, then fill
it in. `clients/` is **gitignored** — client data never enters the public repo.

## Structure

```
clients/<domain.tld>/
├── CLAUDE.md                 # per-client context Claude auto-reads (brand, market, people, tools)
├── _knowledge/               # source material — the client knowledge base
│   ├── audits/               # prior SEO/SEA audits (PDF, docs)
│   ├── keywords/             # target keyword exports (xlsx, csv)
│   ├── calls/                # call notes & transcripts
│   ├── offers/               # previous offers / contracts
│   └── brand/                # client logo, CI, tone-of-voice (if provided)
└── YYYY-MM-DD_<Task>/        # one dated folder per deliverable
    ├── 2026-05-31_Status-Quo/
    ├── 2026-06-07_Potential/
    └── 2026-06-14_Offer/
```

## Rules

1. **One folder per client**, named by domain (`example.com`, not "Example GmbH").
2. **Dated task subfolders** (`YYYY-MM-DD_<Task>`) — never a flat file dump.
3. **`_knowledge/` is read-first.** Before any new deliverable, Claude reads
   `_knowledge/` so it builds on prior work instead of duplicating it.
4. **Per-client `CLAUDE.md`** captures everything that isn't derivable from data:
   decision makers, budget, internal resources, target market, competitors, tools.
   Claude Code reads nested `CLAUDE.md` automatically.
5. **Everything here stays out of git.** Client data is confidential.
