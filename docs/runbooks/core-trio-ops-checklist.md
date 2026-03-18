# Core Trio Ops Checklist

Date: 2026-03-16
Scope: Batch 6A operating baseline for Nexus, Clawver, Cipher

Use this as the fast operational checklist for ticket execution runs.

## Nexus Checklist (Execution Ticket)

1. Create or update task file in `workspace/shared/tasks/CT-XXX.md`.
2. Run pilot bootstrap:
`python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py bootstrap-dispatch --ticket CT-XXX --task-file workspace/shared/tasks/CT-XXX.md`
3. Delegate real work to executor (`qa-agent` or `api-docs-agent`).
4. Wait for executor artifacts in `workspace/shared/test-results/CT-XXX/`.
5. For Stagehand-only tasks, verify guard report exists:
`workspace/shared/test-results/CT-XXX/contracts/stagehand-guard-post.json`
6. Run pre-summary gate:
`python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py pre-summary-gate --ticket CT-XXX`
7. If strict learning sync is required, run:
`python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py pre-summary-gate --ticket CT-XXX --require-learning`
8. Post final summary only from artifact-backed results.

## Clawver Checklist (UI Executor)

1. Read full task and identify Stagehand policy (`ONLY`, `REQUIRED`, `auto`, `off`).
2. Execute requested scope and save evidence under `workspace/shared/test-results/CT-XXX/`.
3. Run legacy mirror sync:
`python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py sync-legacy --ticket CT-XXX`
4. Run fail-fast policy guard:
`python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py stagehand-guard --ticket CT-XXX --phase post --agent qa-agent --on-violation blocked --next-owner nexus --emit-result --write-results-stub`
5. If guard exits with violation, stop and return blocked callback to Nexus.
6. If auth/session was used, register session-record:
`python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py register-session --ticket CT-XXX --project minebit --subject-type player --owner qa-agent --storage-state-ref workspace/shared/test-auth/prod-player-auth.json --token-ref workspace/shared/test-auth/token.txt --status active --refresh-strategy ui_login`
7. Emit result packet:
`python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py emit-result --ticket CT-XXX --agent qa-agent --status completed --confidence medium --next-owner nexus --evidence-ref workspace/shared/test-results/CT-XXX/results.json`
8. Emit learning when reusable finding exists:
`python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py emit-learning --ticket CT-XXX --owner qa-agent --status completed --observed "<observed>" --impact "<impact>" --applies-to "<applies-to>" --promote-to run-only --evidence-ref workspace/shared/test-results/CT-XXX/results.json`

## Cipher Checklist (API/Data Executor)

1. Execute only API/data scope from task or handoff.
2. Save evidence under `workspace/shared/test-results/CT-XXX/`.
3. Run legacy mirror sync:
`python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py sync-legacy --ticket CT-XXX`
4. If session/token artifacts were used, register session-record:
`python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py register-session --ticket CT-XXX --project minebit --subject-type player --owner api-docs-agent --storage-state-ref workspace/shared/test-auth/prod-player-auth.json --token-ref workspace/shared/test-auth/token.txt --status active --refresh-strategy api_refresh`
5. Emit result packet:
`python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py emit-result --ticket CT-XXX --agent api-docs-agent --status completed --confidence medium --next-owner nexus --evidence-ref workspace/shared/test-results/CT-XXX/backend-oauth-test-results.json`
6. Emit learning when reusable finding exists:
`python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py emit-learning --ticket CT-XXX --owner api-docs-agent --status completed --observed "<observed>" --impact "<impact>" --applies-to "<applies-to>" --promote-to run-only --evidence-ref workspace/shared/test-results/CT-XXX/backend-oauth-test-results.json`

## Minimal Artifact Set

1. `workspace/shared/test-results/CT-XXX/results.json` or backend result JSON
2. `workspace/shared/test-results/CT-XXX/contracts/pre-summary-gate.json`
3. `shared/runs/<run_id>/results/*.json`
4. For Stagehand-only tasks: `workspace/shared/test-results/CT-XXX/contracts/stagehand-guard-post.json`
