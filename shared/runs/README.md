# shared/runs

Phase 2 pilot storage for run-centric ticket traceability.

- One active ticket run => one folder: `shared/runs/<run_id>/`
- Active pilot mapping: `shared/runs/active-pilot-runs.json`
- Initialize/sync via:
  - `python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py init --ticket CT-XXX`
  - `python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py sync-legacy --ticket CT-XXX`

Legacy compatibility remains enabled during pilot:

- `workspace/shared/tasks/`
- `workspace/shared/test-results/`
