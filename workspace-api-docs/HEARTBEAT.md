# HEARTBEAT.md - Cipher

Shared reference:

- `/Users/ihorsolopii/.openclaw/docs/architecture/core-trio-shared-standard.md`

## Learning Scan (every 30 minutes)

Check for orphaned results — API execution runs that produced evidence but no learning candidate.

### What to check

1. Scan recent run directories under `workspace/shared/runs/` for Cipher results
2. For each run with `result-packet` but no learning, generate a learning candidate
3. Check `workspace/shared/DAILY_INSIGHTS.md` for today's Cipher entries

### What to do if learning is missing

1. Read the result-packet from the run
2. Extract key API finding (response patterns, error codes, data state)
3. Run `emit-learning` with appropriate `--observed`, `--impact`, `--applies-to`
4. Append summary to `workspace/shared/DAILY_INSIGHTS.md`

## Post-Execution Checkpoint

After every API execution, before sending results back to Nexus:

- [ ] Evidence files saved (API responses, logs)
- [ ] Result packet emitted
- [ ] `emit-learning` executed (mandatory)
- [ ] `DAILY_INSIGHTS.md` updated with one-liner

If any checkbox is unchecked → do not respond to Nexus yet.
