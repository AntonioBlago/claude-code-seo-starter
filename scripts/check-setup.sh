#!/usr/bin/env bash
# Verify the starter is wired up correctly.
set -u

ok=0; fail=0
pass() { echo "  ✓ $1"; ok=$((ok+1)); }
bad()  { echo "  ✗ $1"; fail=$((fail+1)); }
info() { echo "  • $1"; }

echo "Checking Claude Code SEO Starter setup..."

# Tier — the key is OPTIONAL. No key = valid free-tier setup, not a failure.
tier="FREE (keyless — 8 Visibly tools + GSC-export workflow)"
if [ -f .env ] && grep -q '^VISIBLYAI_API_KEY=lc_' .env && ! grep -q 'lc_replace_me' .env; then
  tier="PRO (Visibly key set in .env)"
elif [ -n "${VISIBLYAI_API_KEY:-}" ] && [ "${VISIBLYAI_API_KEY}" != "lc_replace_me" ]; then
  tier="PRO (Visibly key set in environment)"
fi
info "Tier: $tier"

# .mcp.json
[ -f .mcp.json ] && pass ".mcp.json present" || bad ".mcp.json missing"

# hook
if [ -f .claude/hooks/seo-check.sh ]; then
  pass "seo-check.sh hook present"
else
  bad "seo-check.sh hook missing"
fi

# settings
[ -f .claude/settings.json ] && pass ".claude/settings.json present" || bad ".claude/settings.json missing"

# commands
cmds=0
for c in visibly-seo-status-quo visibly-seo-potential visibly-seo-offer visibly-seo-pdf-build; do
  [ -f ".claude/commands/$c.md" ] && cmds=$((cmds+1))
done
[ "$cmds" -eq 4 ] && pass "all 4 slash commands present" || bad "only $cmds/4 slash commands found"

echo ""
echo "Result: $ok passed, $fail failed.  Tier: $tier"
if [ "$fail" -eq 0 ]; then
  echo "All good — run 'claude' and try /visibly-seo-status-quo example.com"
  case "$tier" in PRO*) : ;; *) echo "(Free tier: feed a GSC export to the Python templates, or add a key — see docs/setup.md §3.)" ;; esac
else
  echo "Fix the items above, then re-run."
fi
exit "$fail"
