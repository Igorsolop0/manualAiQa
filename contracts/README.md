# Contracts Layer (Phase 1)

This folder introduces canonical handoff contracts for OpenClaw.

## Schemas

- `task-charter.schema.json`
- `handoff-packet.schema.json`
- `result-packet.schema.json`
- `session-record.schema.json`
- `knowledge-card.schema.json`
- `ambiguity-report.schema.json`

## Examples

Examples are in `contracts/examples/` and represent a mixed Minebit-like UI+API scenario (deposit streak / bonus visibility).

## Lightweight validation

Run from repository root:

```bash
bash contracts/validate-examples.sh
```

The helper uses `npx ajv-cli` and validates each example against its schema.
If `npx` is unavailable, install Node.js first or validate with your preferred JSON Schema tool.

## Phase 2 pilot note

For run-centric dual-write pilot scaffolding, use:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py init --ticket CT-XXX --project minebit
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py sync-legacy --ticket CT-XXX
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py register-session --ticket CT-XXX --project minebit --subject-type player --owner qa-agent --storage-state-ref workspace/shared/test-auth/prod-player-auth.json --token-ref workspace/shared/test-auth/token.txt --status active --refresh-strategy ui_login
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py emit-result --ticket CT-XXX --agent qa-agent --status completed --confidence medium --next-owner nexus --evidence-ref workspace/shared/test-results/CT-XXX/results.json
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py prepare-dispatch --ticket CT-XXX --agent qa-agent --task-file workspace/shared/tasks/CT-XXX.md
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py bootstrap-dispatch --ticket CT-XXX --task-file workspace/shared/tasks/CT-XXX.md
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py pre-summary-gate --ticket CT-XXX
```
