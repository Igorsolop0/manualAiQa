---
name: auto-learn
description: |
  Automatic learning capture after every execution. Scans recent activity,
  extracts insights, and emits learning candidates via phase2_pilot.py.
  Ensures Clawver never finishes a run without recording what was learned.
activation: |
  Triggered automatically:
  1. After every task execution (before responding to Nexus)
  2. Via HEARTBEAT 30-min scan (if results exist without learnings)
  3. Manually via /auto-learn
---

# Auto-Learn Skill

## Philosophy

**"No run without a learning."**

Every execution produces knowledge — even if it confirms existing behavior.
This skill ensures that knowledge is captured immediately, not forgotten.

## When This Runs

### Trigger 1: Post-Execution (mandatory)

After completing any task execution and before responding to Nexus:

1. Review what was done during this execution
2. Extract key observations
3. Emit learning via `phase2_pilot.py emit-learning`

### Trigger 2: HEARTBEAT Scan (every 30 min)

Check for orphaned results — runs that completed but have no learning:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py scan-missing-learnings
```

If missing learnings found → generate and emit them from available evidence.

### Trigger 3: Manual

Run `/auto-learn` to force a scan of recent activity.

## Post-Execution Learning Capture

After every execution, before responding to Nexus, follow this sequence:

### Step 1: Identify what was learned

Ask yourself:
- Did I discover something about the UI that wasn't documented?
- Did I find a blocker or unexpected behavior?
- Did auth work as expected?
- Did I find elements/selectors that could be reused?
- Did the test flow match expectations or diverge?

### Step 2: Classify the learning

| Type | Example | promote-to |
|------|---------|------------|
| New UI behavior | "Deposit modal requires 2-click confirmation" | project |
| Blocker found | "Auth token expired after 10 minutes" | project |
| Selector discovery | "Bonus button ref=e26 in nav bar" | run-only |
| Expected behavior confirmed | "Login flow works as documented" | run-only |
| Environment issue | "QA env returns 502 on /api/bonuses" | project |
| Auth pattern | "Token must be in cookie, not hash" | agent |

### Step 3: Emit the learning

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py emit-learning \
  --ticket <TICKET> \
  --owner qa-agent \
  --status completed \
  --observed "<what you saw>" \
  --impact "<why it matters>" \
  --applies-to "<project/feature/flow>" \
  --promote-to <run-only|project|agent> \
  --evidence-ref workspace/shared/test-results/<TICKET>/results.json
```

### Step 4: Write to DAILY_INSIGHTS.md

Append a one-liner to `workspace/shared/DAILY_INSIGHTS.md`:

```markdown
- **<TICKET>** (<date>): <one-line summary of learning> — `<promote-to>`
```

## Learning Templates

### When execution found something new:
```
--observed "Telegram auth token link shows 'Log In' button instead of user profile — token in URL hash is not picked up by the app"
--impact "Auth via hash fragment may be broken or require different implementation"
--applies-to "minebit/auth/telegram-token"
--promote-to project
```

### When execution confirmed expectations:
```
--observed "execution matched expectations, no new findings"
--impact "confirms existing knowledge"
--applies-to "minebit/<feature>"
--promote-to run-only
```

### When execution was blocked:
```
--observed "Could not complete test — QA environment returned 502 on bonus API"
--impact "Environment instability blocks QA execution"
--applies-to "minebit/environment/qa"
--promote-to project
```

## Auto-Promote Rules

Learnings that appear 3+ times across different tickets in 7 days should be promoted:

| Current level | Promote to | Condition |
|---------------|------------|-----------|
| run-only | project | Same pattern in 3+ runs within 7 days |
| project | agent | Pattern applies across projects/features |
| agent | MEMORY.md | Fundamental operational knowledge |

Demotion: if a learning hasn't been referenced in 30+ days, it stays but gets tagged `[stale]`.

## Integration with phase2_pilot.py

The `pre-summary-gate --require-learning` command will **block** Nexus from posting a summary if no learning was emitted. This is the enforcement mechanism.

If Clawver skips auto-learn → Nexus gets blocked → Ihor gets alerted.

## Evidence Files That Inform Learnings

When generating a learning, look at these artifacts:

- `results.json` — overall pass/fail and findings
- `step-*-snapshot.yml` — accessibility trees showing page state
- `step-*.png` — visual evidence
- `network-log.txt` — API responses and errors
- `console-log.txt` — JavaScript errors
- `.playwright-cli/console-*.log` — browser console
- `.playwright-cli/page-*.yml` — page snapshots
