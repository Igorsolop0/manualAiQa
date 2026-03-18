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
  - `scripts/run_manager.py` (`init`, `sync-legacy`, `register-session`, `emit-result`, `prepare-dispatch`)
- Added runbook:
  - `docs/runbooks/phase2-pilot-dual-write.md`
- Migration mode is dual-write for selected tickets only:
  - legacy `workspace/shared/*` stays active,
  - run folder acts as traceability mirror.

## Open TODO (added 2026-03-13)

1. [x] Add result-ready gate for Nexus before Slack summary.
   - Problem: transient ENOENT race when reading `workspace/shared/test-results/<ticket>/results.json`.
   - Observed example: `2026-03-13 16:37:24` read attempt for `CT-752` before file creation (`16:46:43`).
   - Implemented via: `run_manager.py pre-summary-gate` (wait + stability check + report).
2. [x] Enforce Phase 2 pilot bootstrap for selected CT tickets.
   - Require `run_manager.py init` + `prepare-dispatch` at task creation time.
   - Implemented via: `run_manager.py bootstrap-dispatch` (init-if-missing + dispatch block).
3. [x] Add pre-summary contract validation gate in pilot flow.
   - Validate emitted `result-packet` and (if used) `session-record` before final Nexus summary.
   - Implemented via: `run_manager.py pre-summary-gate` (`ajv-cli` contract validation).
4. [x] Batch 1.5: Nexus MEMORY cleanup.
   - Reduced `workspace/MEMORY.md` into compact operational memory.
   - Preserved durable orchestration truths and recurring failure patterns.
   - Archived previous long-form version to `docs/archive/legacy/workspace-root/MEMORY-2026-03-15-pre-cleanup.md`.

## Phase 3 status checkpoint (2026-03-15)

Phase 3 is in progress and has a stable documentation baseline now.

Completed so far:

- core trio file-meaning standard is aligned
- shared QA cognition layer was drafted in `docs/architecture/qa-operating-framework.md`
- shared learning sync model was drafted in `docs/architecture/learning-sync-model.md`
- refactor run review checklist was added in `docs/architecture/refactor-compliance-checklist.md`
- Nexus, Clawver, and Cipher startup guides were cleaned up
- Nexus, Clawver, and Cipher `SOUL.md` files were narrowed to role, boundaries, stop rules, and evidence rules
- shared communication model was documented in `docs/architecture/core-trio-shared-standard.md`
- safe archival cleanup removed legacy noise from top-level `workspace/` and `workspace-qa-agent/`
- actual startup/runtime file usage was documented in `docs/architecture/agent-reference-map.md`
- Nexus `MEMORY.md` was reduced to operational memory only
- ticket naming was normalized to canonical `CT-XXX` across pilot helper and Stagehand artifact fallback paths
- layered test-design profile extracted from `workspace/QA_TEST_DESIGN_APPROACH.md` into canonical architecture docs

Still open in Phase 3:

- Stagehand drift hardening now has fail-fast guard (`run_manager.py stagehand-guard`) for `Stagehand ONLY` violations
- roll out updated dispatch block via `bootstrap-dispatch` on new execution tasks to apply guard consistently
- learning emission hardening is now implemented in pilot helper (`run_manager.py emit-learning` + gate visibility in `pre-summary-gate`)
- Batch 6A baseline checklist added: `docs/runbooks/core-trio-ops-checklist.md`
- adopt `pre-summary-gate --require-learning` on selected runs after 1-2 dry runs confirm signal/noise balance
- use the refactor compliance checklist on more live runs and convert repeated failures into explicit guardrails
- optionally do another pass on project-specific memory placement if new duplication appears
