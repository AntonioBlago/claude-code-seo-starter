#!/usr/bin/env bash
# Verify the starter is wired up correctly.
set -u

ok=0; fail=0
pass() { echo "  ✓ $1"; ok=$((ok+1)); }
bad()  { echo "  ✗ $1"; fail=$((fail+1)); }

echo "Checking Claude Code SEO Starter setup..."

# .env
if [ -f .env ]; then
  pass ".env exists"
  if grep -q '^VISIBLY_AI_API_KEY=lc_' .env && ! grep -q 'lc_replace_me' .env; then
    pass "VISIBLY_AI_API_KEY looks set"
  else
    bad "VISIBLY_AI_API_KEY not set (edit .env, paste your lc_... key)"
  fi
else
  bad ".env missing — run: cp .env.example .env"
fi

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
for c in status-quo potenzial angebot pdf-build; do
  [ -f ".claude/commands/$c.md" ] && cmds=$((cmds+1))
done
[ "$cmds" -eq 4 ] && pass "all 4 slash commands present" || bad "only $cmds/4 slash commands found"

echo ""
echo "Result: $ok passed, $fail failed."
[ "$fail" -eq 0 ] && echo "All good — run 'claude' and try /status-quo example.com" || echo "Fix the items above, then re-run."
exit "$fail"
