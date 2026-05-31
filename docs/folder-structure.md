# Folder structure & conventions

A consistent structure is what lets Claude (and you) build on prior work instead of
re-doing it. Two pillars: a **client knowledge base** per client, and a shared **CI base**.

## Repo-level layout

```
claude-code-seo-starter/
├── CLAUDE.md                 # global project context Claude reads every run
├── .claude/                  # commands, skills, hooks, settings
├── docs/                     # methodology (this file, workflows, ctr-model, best-practices)
├── templates/
│   ├── ci/                   # CI base — brand.py + CI.md (your corporate identity)
│   ├── client-template/      # copy → clients/<domain>/ for each new client
│   └── pdf_example.py        # CI-compliant PDF starter
└── clients/                  # ← gitignored. All client data lives here, never in git.
```

## Client knowledge base (per client)

Copy `templates/client-template/` to `clients/<domain.tld>/` for every client:

```
clients/<domain.tld>/
├── CLAUDE.md                 # per-client context (auto-read by Claude Code)
├── _knowledge/               # read-first source material
│   ├── audits/  keywords/  calls/  offers/  brand/
└── YYYY-MM-DD_<Task>/        # one dated folder per deliverable
```

### Rules

1. **One folder per client**, named by domain (`example.com`) — not by company name.
2. **Dated task subfolders** `YYYY-MM-DD_<Task>` — never a flat dump of files.
3. **`_knowledge/` is read-first.** Claude reads it before any new deliverable so it
   recognises and extends prior work (the #1 trust signal with clients).
4. **Per-client `CLAUDE.md`** holds everything not derivable from data — decision
   makers, budget, market, competitors, stack, constraints. Claude Code reads nested
   `CLAUDE.md` automatically.
5. **Client data stays out of git.** `clients/` is in `.gitignore`. Confidential by default.

## CI base (shared across all clients)

Your corporate identity lives in one place — `templates/ci/`:

- **`brand.py`** — machine-readable constants (colours, fonts, contact). Import it
  everywhere instead of hard-coding hex values: `from templates.ci.brand import PRIMARY`.
- **`CI.md`** — human-readable reference Claude reads when producing documents.

Keep the two in sync. Centralising the CI means a rebrand is a one-file change, and
every PDF/Excel/Markdown export stays consistent. Your **filled-in** CI and any
sensitive assets (signatures, bank details, licensed logos) belong in a **private**
location — never in a public repo.
