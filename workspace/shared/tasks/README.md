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
```
