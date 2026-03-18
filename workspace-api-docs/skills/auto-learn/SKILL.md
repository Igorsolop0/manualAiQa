---
name: auto-learn
description: |
  Automatic learning capture after every API execution. Scans recent activity,
  extracts insights, and emits learning candidates via phase2_pilot.py.
  Ensures Cipher never finishes a run without recording what was learned.
activation: |
  Triggered automatically:
  1. After every task execution (before responding to Nexus)
  2. Via HEARTBEAT 30-min scan (if results exist without learnings)
  3. Manually via /auto-learn
---

# Auto-Learn Skill (Cipher)

## Philosophy

**"No run without a learning."**

Every API execution produces knowledge — even if it confirms existing behavior.

## Post-Execution Learning Capture

After every execution, before responding to Nexus:

### Step 1: Identify what was learned

- Did API responses match expected schema?
- Did error codes reveal unexpected behavior?
- Did data preparation work as expected?
- Did auth/session handling require workarounds?
- Were there rate limits, timeouts, or environment issues?

### Step 2: Classify and emit

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py emit-learning \
  --ticket <TICKET> \
  --owner api-docs-agent \
  --status completed \
  --observed "<what you saw>" \
  --impact "<why it matters>" \
  --applies-to "<project/api/service>" \
  --promote-to <run-only|project|agent> \
  --evidence-ref workspace/shared/test-results/<TICKET>/results.json
```

### Step 3: Update DAILY_INSIGHTS.md

```markdown
- **<TICKET>** (<date>): <one-line summary> — `<promote-to>`
```

## Learning Templates

### API behavior discovery:
```
--observed "BonusCalculationService returns 400 when deposit amount is 0, but 200 with null"
--impact "Null vs zero handling inconsistency in bonus API"
--applies-to "platform/bonus-calculation-service"
--promote-to project
```

### Expected behavior confirmed:
```
--observed "execution matched expectations, no new findings"
--impact "confirms existing knowledge"
--applies-to "platform/<service>"
--promote-to run-only
```
