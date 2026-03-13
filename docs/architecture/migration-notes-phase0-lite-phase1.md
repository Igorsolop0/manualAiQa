# Migration Notes - Phase 0-lite + Phase 1

Date: 2026-03-13
Status: additive rollout (no destructive migration)

## Compatibility shim

- Active execution flows remain on legacy workspace paths:
- `workspace/shared/tasks/`
- `workspace/shared/credentials/`
- `workspace/shared/test-results/`

- New governance and contracts are added at repository root:
- `shared/registry/`
- `contracts/`
- `docs/architecture/`
- `docs/specs/`

## Why this is safe

- No existing runtime folder was removed.
- No existing agent execution path was deleted.
- Nexus docs gained routing guardrails (`capability + maturity`) without full persona rewrite.

## Planned next migration step

- Introduce `shared/runs/<run_id>/` and `shared/sessions/registry.json` (Phase 2),
  then progressively map legacy outputs into run-centric folders.

## Phase 2 pilot bootstrap (2026-03-13)

- Added pilot scaffolding:
  - `shared/runs/`
  - `shared/sessions/registry.json`
- Added pilot automation helper:
  - `scripts/phase2_pilot.py` (`init`, `sync-legacy`, `register-session`, `emit-result`, `prepare-dispatch`)
- Added runbook:
  - `docs/runbooks/phase2-pilot-dual-write.md`
- Migration mode is dual-write for selected tickets only:
  - legacy `workspace/shared/*` stays active,
  - run folder acts as traceability mirror.

## Open TODO (added 2026-03-13)

1. [x] Add result-ready gate for Nexus before Slack summary.
   - Problem: transient ENOENT race when reading `workspace/shared/test-results/<ticket>/results.json`.
   - Observed example: `2026-03-13 16:37:24` read attempt for `CT-752` before file creation (`16:46:43`).
   - Implemented via: `phase2_pilot.py pre-summary-gate` (wait + stability check + report).
2. [x] Enforce Phase 2 pilot bootstrap for selected CT tickets.
   - Require `phase2_pilot.py init` + `prepare-dispatch` at task creation time.
   - Implemented via: `phase2_pilot.py bootstrap-dispatch` (init-if-missing + dispatch block).
3. [x] Add pre-summary contract validation gate in pilot flow.
   - Validate emitted `result-packet` and (if used) `session-record` before final Nexus summary.
   - Implemented via: `phase2_pilot.py pre-summary-gate` (`ajv-cli` contract validation).
