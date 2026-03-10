# Task Delegation Store

This directory contains explicit, task-based instructions from Nexus to specialized agents (like QA Agent or API Docs Agent).

## Format
Task files should be named `[TICKET_ID]-task.md` (e.g., `CT-476-task.md`).

## Template
```markdown
# Task: Smoke Test CT-476
- **Environment:** https://minebit-casino.prod.sofon.one
- **Auth:** Required. Read credentials from `workspace/shared/credentials/CT-476-prod-credentials.json`
- **Scenarios:**
  1. `cashierstep=depositcrypto`
  2. `cashierstep=buycrypto`
- **Success criteria:** Modal opens successfully for authorized user.
- **Save to:** `workspace/shared/test-results/CT-476/`
```
