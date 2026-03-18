# Task Delegation Store

This directory contains explicit, task-based instructions from Nexus to specialized agents (like QA Agent or API Docs Agent).

## Format
Task files should be named `[TICKET_ID]-task.md` (e.g., `CT-476-task.md`).
Use canonical ticket casing in paths: `CT-XXX` (not `ct-xxx`).

## Template
```markdown
# Task: Smoke Test CT-476
- **Source ticket or charter:** CT-476
- **Prepared by:** Nexus
- **Context retrieval notes:**
  - Related prior flow or ticket: [if found]
  - Existing assets checked: [fixtures/scripts/tests/helpers/session refs]
  - Important missing context: [if any]
- **Feature framing:**
  - Behavior under test: [what changed]
  - User-visible goal: [what should happen]
  - Key dependency: [backend/auth/data dependency]
- **Risk focus:**
  1. [highest risk]
  2. [second risk]
- **Environment:** https://minebit-casino.prod.sofon.one
- **Auth:** Required. Read credentials from `workspace/shared/credentials/CT-476-prod-credentials.json`
- **Browser tool:** `playwright-cli` (default for all browser tasks)
- **Execution owner:** `qa-agent` (`qa-agent|api-docs-agent|mixed`)
- **Execution split:**
  - Clawver: [browser or UI scope]
  - Cipher: [API or data-prep scope, if any]
- **Browser goals:**
  1. Start URL: [exact URL]
  2. Expected final state: [what should be visible/confirmed]
  3. Key elements to capture: [forms, buttons, modals to document]
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
python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py sync-legacy --ticket CT-476
```

If auth/session was used, register session-record (no raw token in prose):
```bash
python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py register-session --ticket CT-476 --project minebit --subject-type player --owner qa-agent --storage-state-ref workspace/shared/test-auth/prod-player-auth.json --token-ref workspace/shared/test-auth/token.txt --status active --refresh-strategy ui_login
```

Emit result packet:
```bash
python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py emit-result --ticket CT-476 --agent qa-agent --status completed --confidence medium --next-owner nexus --evidence-ref workspace/shared/test-results/CT-476/results.json
```

Emit learning candidate (when run produced reusable finding):
```bash
python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py emit-learning --ticket CT-476 --owner qa-agent --status completed --observed "<observed>" --impact "<impact>" --applies-to "<applies-to>" --promote-to run-only --evidence-ref workspace/shared/test-results/CT-476/results.json
```
<!-- PHASE2_DISPATCH_BLOCK_END -->
```

## Auto-insert dispatch block

Nexus can auto-insert/update the Phase 2 block into any task file:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py prepare-dispatch --ticket CT-XXX --agent qa-agent --task-file workspace/shared/tasks/CT-XXX.md
python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py prepare-dispatch --ticket CT-XXX --agent api-docs-agent --task-file workspace/shared/tasks/CT-XXX.md
```

Recommended for Nexus (enforce init + dispatch in one command):

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py bootstrap-dispatch --ticket CT-XXX --task-file workspace/shared/tasks/CT-XXX.md
```

For new `CT-*` execution tasks, this should be treated as the default path, not an optional extra.
Analysis-only ticket summaries do not need pilot bootstrap.

API-only variant:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py bootstrap-dispatch --ticket CT-XXX --task-file workspace/shared/tasks/CT-XXX.md --agent api-docs-agent
```

Before final Slack summary in pilot mode:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py pre-summary-gate --ticket CT-XXX
```

If you want strict enforcement of learning sync:

```bash
python3 /Users/ihorsolopii/.openclaw/scripts/run_manager.py pre-summary-gate --ticket CT-XXX --require-learning
```

`pre-summary-gate` now also checks runtime policy violations for pilot runs.

## Nexus planning expectation

Before creating a task file, Nexus should usually structure the planning output as:

1. `Context Retrieval`
2. `Feature Framing`
3. `Risk Focus`
4. `Execution Split`
5. `Test Plan`
6. `Approval / Next Action`

Task files should reflect that structure in compact form instead of starting directly with scenarios only.
