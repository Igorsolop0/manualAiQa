# HEARTBEAT.md - Clawver

Shared reference:

- `/Users/ihorsolopii/.openclaw/docs/architecture/core-trio-shared-standard.md`

## Learning Scan (every 30 minutes)

Check for orphaned results — runs that produced evidence but no learning candidate.

### What to check

1. Scan `workspace/shared/test-results/` for folders modified in the last 60 minutes
2. For each folder with `results.json`, check if a corresponding `emit-learning` was run
3. If learning is missing → generate it from available evidence

### How to check

```bash
# List recent test results without learnings
for dir in workspace/shared/test-results/CT-*/; do
  ticket=$(basename "$dir")
  results="$dir/results.json"
  if [ -f "$results" ]; then
    # Check if learning exists in the run
    run_id=$(python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py verify-run --ticket "$ticket" 2>/dev/null | grep "run_id=" | cut -d= -f2)
    if [ -n "$run_id" ]; then
      learning_dir="workspace/shared/runs/$run_id/learning"
      if [ ! -d "$learning_dir" ] || [ -z "$(ls -A "$learning_dir" 2>/dev/null)" ]; then
        echo "MISSING LEARNING: $ticket (run: $run_id)"
      fi
    fi
  fi
done
```

### What to do if learning is missing

1. Read `results.json` from the evidence folder
2. Read any screenshots or snapshots
3. Extract the key finding (even if it's "everything worked as expected")
4. Run `emit-learning` with appropriate `--observed`, `--impact`, `--applies-to`
5. Append summary to `workspace/shared/DAILY_INSIGHTS.md`

## Post-Execution Checkpoint

After every task execution, before sending results back to Nexus:

- [ ] Evidence files saved to correct path
- [ ] `results.json` written
- [ ] `emit-learning` executed (mandatory)
- [ ] `DAILY_INSIGHTS.md` updated with one-liner

If any checkbox is unchecked → do not respond to Nexus yet.
