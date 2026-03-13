# Task Delegation Store

This directory contains explicit, task-based instructions from Nexus to specialized agents (like QA Agent or API Docs Agent).

## Format
Task files should be named `[TICKET_ID]-task.md` (e.g., `CT-476-task.md`).

## Template
```markdown
# Task: Smoke Test CT-476
- **Environment:** https://minebit-casino.prod.sofon.one
- **Auth:** Required. Read credentials from `workspace/shared/credentials/CT-476-prod-credentials.json`
- **Stagehand mode:** auto (`auto|required|off`)
- **Browser goals (only if Stagehand mode != off):**
  1. Reach state: [expected final UI state]
  2. Start URL: [exact URL]
  3. Max steps/timeout: [e.g. 25 / 90000ms]
- **Knowledge output target:** `workspace/projects/nextcode/docs/ui-knowledge/minebit/`
- **Scenarios:**
  1. `cashierstep=depositcrypto`
  2. `cashierstep=buycrypto`
- **Success criteria:** Modal opens successfully for authorized user.
- **Save to:** `workspace/shared/test-results/CT-476/`

<!-- PHASE2_DISPATCH_BLOCK_START -->
## Phase 2 Pilot Dispatch Hooks (Auto-generated)
- **run_id:** `CT-476-YYYYMMDD-01`
- **agent:** `qa-agent` (or `api-docs-agent`)
- **mode:** `dual-write` (legacy + run mirror)

After execution, run mirror sync:
```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py sync-legacy --ticket CT-476
```

If auth/session was used, register session-record (no raw token in prose):
```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py register-session --ticket CT-476 --project minebit --subject-type player --owner qa-agent --storage-state-ref workspace/shared/test-auth/prod-player-auth.json --token-ref workspace/shared/test-auth/token.txt --status active --refresh-strategy ui_login
```

Emit result packet:
```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py emit-result --ticket CT-476 --agent qa-agent --status completed --confidence medium --next-owner nexus --evidence-ref workspace/shared/test-results/CT-476/results.json
```
<!-- PHASE2_DISPATCH_BLOCK_END -->
```

## Auto-insert dispatch block

Nexus can auto-insert/update the Phase 2 block into any task file:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py prepare-dispatch --ticket CT-XXX --agent qa-agent --task-file workspace/shared/tasks/CT-XXX.md
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py prepare-dispatch --ticket CT-XXX --agent api-docs-agent --task-file workspace/shared/tasks/CT-XXX.md
```

Recommended for Nexus (enforce init + dispatch in one command):

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py bootstrap-dispatch --ticket CT-XXX --task-file workspace/shared/tasks/CT-XXX.md
```

API-only variant:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py bootstrap-dispatch --ticket CT-XXX --task-file workspace/shared/tasks/CT-XXX.md --agent api-docs-agent
```

Before final Slack summary in pilot mode:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/phase2_pilot.py pre-summary-gate --ticket CT-XXX
```
