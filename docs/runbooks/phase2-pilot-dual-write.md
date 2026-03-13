# Phase 2 Pilot Runbook - Dual-Write (Run-Centric + Legacy)

Date: 2026-03-13  
Scope: Safe pilot for one ticket at a time.

## Goal

Keep current behavior (`workspace/shared/*`) while introducing per-ticket run traceability in:

- `shared/runs/<run_id>/`
- `shared/sessions/registry.json`

## Why this is safe

- Legacy paths remain active.
- No existing task/evidence path is removed.
- Pilot is opt-in per ticket.

## Commands

Initialize pilot run for one ticket:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py init --ticket CT-XXX --project minebit
```

Initialize and immediately mirror existing legacy evidence:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py init --ticket CT-XXX --project minebit --sync-legacy
```

Sync legacy evidence into active run after Clawver/Cipher finished:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py sync-legacy --ticket CT-XXX
```

Or explicitly by run_id:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py sync-legacy --run-id CT-XXX-YYYYMMDD-01
```

Register session-record (instead of raw token handoff):

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py register-session --ticket CT-XXX --project minebit --subject-type player --owner qa-agent --storage-state-ref workspace/shared/test-auth/prod-player-auth.json --token-ref workspace/shared/test-auth/token.txt --status active --refresh-strategy ui_login
```

Emit result-packet from executor:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py emit-result --ticket CT-XXX --agent qa-agent --status completed --confidence medium --next-owner nexus --evidence-ref workspace/shared/test-results/CT-XXX/results.json
```

Auto-insert hooks into task file:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py prepare-dispatch --ticket CT-XXX --agent qa-agent --task-file workspace/shared/tasks/CT-XXX.md
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py prepare-dispatch --ticket CT-XXX --agent api-docs-agent --task-file workspace/shared/tasks/CT-XXX.md
```

Preferred one-shot bootstrap (init if missing + dispatch hooks):

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py bootstrap-dispatch --ticket CT-XXX --task-file workspace/shared/tasks/CT-XXX.md
```

For API-only ticket handoff:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py bootstrap-dispatch --ticket CT-XXX --task-file workspace/shared/tasks/CT-XXX.md --agent api-docs-agent
```

Pre-summary gate before Nexus posts Slack result:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py pre-summary-gate --ticket CT-XXX
```

## What gets created

- `shared/runs/<run_id>/` folders:
  - `intake/`, `plan/`, `handoffs/`, `sessions/`, `evidence/ui/`, `evidence/api/`, `evidence/legacy-mirror/`, `results/`, `learning/`, `meta/`
- `plan/task-charter.json`
- `handoffs/nexus-to-clawver.json`
- `handoffs/nexus-to-cipher.json`
- `meta/run-manifest.json`
- `meta/legacy-sync-report.json` (after sync)
- `shared/runs/active-pilot-runs.json`
- `shared/sessions/registry.json`
- Legacy compatibility:
  - `workspace/shared/test-results/CT-XXX/RUN_ID.txt`
  - `workspace/shared/test-results/CT-XXX/contracts/` (contract exports + sync report)

## Pilot operating rules

1. Nexus still writes task file into legacy `workspace/shared/tasks/`.
2. Clawver/Cipher still write evidence into legacy `workspace/shared/test-results/<ticket>/`.
3. After each executor pass, Nexus (or executor) runs `sync-legacy`.
4. Session handoff is by `session-record` refs (no raw token in prose).
5. Executors emit `result-packet` into run contracts.
6. Nexus reviews run folder as canonical trace for pilot ticket.
7. Before Slack summary, Nexus waits for `results.json` readiness.
   - Use retry with short backoff until file exists and timestamp is stable.
   - If not ready by timeout, return partial status with explicit "result not finalized".
8. Before Slack summary in pilot mode, run contract validation.
   - Validate `result-packet` and `session-record` (when present).
   - If invalid, mark summary as `PARTIAL` and include validation error.

## Exit criteria for pilot

- 2-3 tickets completed without breaking legacy flow.
- Each ticket has both:
  - complete legacy evidence,
  - complete run mirror (`shared/runs/<run_id>/evidence/legacy-mirror/`).

Then we can disable dual-write and move to run-primary mode in next phase.
